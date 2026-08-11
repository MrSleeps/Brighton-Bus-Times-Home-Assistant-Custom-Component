"""Data update coordinator for Brighton Bus Times."""

from __future__ import annotations

from datetime import timedelta
import logging
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import BusTimesApiClient, BusTimesApiError
from .const import CONF_SCAN_INTERVAL, CONF_STOP_IDS, DEFAULT_SCAN_INTERVAL, DOMAIN

_LOGGER = logging.getLogger(__name__)


class BusTimesDataUpdateCoordinator(DataUpdateCoordinator[dict[str, Any]]):
    """Fetch all stops together to minimise requests."""

    def __init__(
        self,
        hass: HomeAssistant,
        entry: ConfigEntry,
        client: BusTimesApiClient,
    ) -> None:
        self.entry = entry
        self.client = client
        scan_interval = entry.options.get(
            CONF_SCAN_INTERVAL,
            entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )
        super().__init__(
            hass,
            logger=_LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=scan_interval),
        )

    @property
    def stop_ids(self) -> list[str]:
        """Return currently configured stop IDs."""
        return self.entry.options.get(CONF_STOP_IDS, self.entry.data[CONF_STOP_IDS])

    async def _async_update_data(self) -> dict[str, Any]:
        try:
            return await self.client.async_get_departures(self.stop_ids)
        except BusTimesApiError as err:
            raise UpdateFailed("Unable to update bus departures") from err
