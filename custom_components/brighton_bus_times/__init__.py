"""Brighton Bus Times integration."""

from __future__ import annotations

import logging
from pathlib import Path

from homeassistant.components.http import StaticPathConfig
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_URL, Platform
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession
import homeassistant.helpers.config_validation as cv

from .api import BusTimesApiClient
from .const import DOMAIN
from .coordinator import BusTimesDataUpdateCoordinator

CONFIG_SCHEMA = cv.config_entry_only_config_schema(DOMAIN)

PLATFORMS = [Platform.SENSOR]

_LOGGER = logging.getLogger(__name__)

CARD_URL = "/brighton_bus_times/brighton-bus-times-card.js"
CARD_PATH = Path(__file__).parent / "frontend" / "brighton-bus-times-card.js"

type BusTimesConfigEntry = ConfigEntry[BusTimesDataUpdateCoordinator]


async def async_setup(hass: HomeAssistant, config: dict) -> bool:
    """Serve and register the bundled Lovelace card."""
    await hass.http.async_register_static_paths(
        [StaticPathConfig(CARD_URL, str(CARD_PATH), False)]
    )

    try:
        lovelace = hass.data.get("lovelace")
        resources = getattr(lovelace, "resources", None)

        if resources is None:
            _LOGGER.warning(
                "Lovelace resources are unavailable; add %s manually",
                CARD_URL,
            )
            return True

        if not resources.loaded:
            await resources.async_load()

        existing_resources = resources.async_items()
        card_already_registered = any(
            str(item.get("url", "")).split("?", 1)[0] == CARD_URL
            for item in existing_resources
        )

        if not card_already_registered:
            await resources.async_create_item(
                {
                    "res_type": "module",
                    "url": CARD_URL,
                }
            )
    except Exception: 
        _LOGGER.exception(
            "Unable to register the bundled Lovelace card; add %s manually",
            CARD_URL,
        )

    return True


async def async_setup_entry(hass: HomeAssistant, entry: BusTimesConfigEntry) -> bool:
    """Set up Brighton Bus Times from a config entry."""
    client = BusTimesApiClient(async_get_clientsession(hass), entry.data[CONF_URL])
    coordinator = BusTimesDataUpdateCoordinator(hass, entry, client)
    await coordinator.async_config_entry_first_refresh()
    entry.runtime_data = coordinator
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    entry.async_on_unload(entry.add_update_listener(async_reload_entry))
    return True

async def async_unload_entry(hass: HomeAssistant, entry: BusTimesConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def async_reload_entry(hass: HomeAssistant, entry: BusTimesConfigEntry) -> None:
    """Reload after options change."""
    await hass.config_entries.async_reload(entry.entry_id)
