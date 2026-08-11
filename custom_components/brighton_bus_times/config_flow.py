"""Config flow for Brighton Bus Times."""

from __future__ import annotations

from typing import Any

import voluptuous as vol

from homeassistant.config_entries import ConfigEntry, ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.const import CONF_URL
from homeassistant.core import callback
from homeassistant.helpers import selector
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import (
    BusTimesApiClient,
    BusTimesConnectionError,
    BusTimesInvalidResponseError,
    BusTimesInvalidStopsError,
)
from .const import (
    CONF_SCAN_INTERVAL,
    CONF_STOP_IDS,
    CONF_STOP_QUERY,
    DEFAULT_BASE_URL,
    DEFAULT_SCAN_INTERVAL,
    DOMAIN,
    MAX_SCAN_INTERVAL,
    MIN_SCAN_INTERVAL,
)


def _normalise_stop_ids(value: str | list[str]) -> list[str]:
    """Turn comma/newline separated stop IDs into a unique list."""
    if isinstance(value, list):
        raw = value
    else:
        raw = value.replace("\n", ",").split(",")
    return list(dict.fromkeys(item.strip() for item in raw if item.strip()))


def _schema(
    default_url: str,
    default_query: str,
    default_stops: list[str],
    default_interval: int,
) -> vol.Schema:
    return vol.Schema(
        {
            vol.Required(CONF_URL, default=default_url): str,
            vol.Optional(CONF_STOP_QUERY, default=default_query): str,
            vol.Optional(
                CONF_STOP_IDS,
                default=", ".join(default_stops),
            ): str,
            vol.Required(
                CONF_SCAN_INTERVAL,
                default=default_interval,
            ): vol.All(vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL)),
        }
    )


async def _validate_input(hass, user_input: dict[str, Any]) -> tuple[list[str], dict[str, Any]]:
    stop_ids = _normalise_stop_ids(user_input[CONF_STOP_IDS])
    if not stop_ids:
        raise BusTimesInvalidStopsError([])
    client = BusTimesApiClient(async_get_clientsession(hass), user_input[CONF_URL])
    payload = await client.async_validate_stops(stop_ids)
    return stop_ids, payload


class BusTimesConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle initial setup."""

    VERSION = 1

    def __init__(self) -> None:
        self._pending_url = DEFAULT_BASE_URL
        self._pending_interval = DEFAULT_SCAN_INTERVAL
        self._search_results: list[dict[str, str]] = []

    async def async_step_user(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        """Handle the user step."""
        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = {}

        if user_input is not None:
            query = str(user_input.get(CONF_STOP_QUERY, "")).strip()
            manual_stop_ids = _normalise_stop_ids(user_input.get(CONF_STOP_IDS, ""))

            if manual_stop_ids:
                try:
                    stop_ids, payload = await _validate_input(self.hass, user_input)
                except BusTimesInvalidStopsError as err:
                    errors["base"] = "invalid_stops"
                    description_placeholders["invalid_stops"] = ", ".join(err.stop_ids) or "None supplied"
                except BusTimesConnectionError:
                    errors["base"] = "cannot_connect"
                except BusTimesInvalidResponseError:
                    errors["base"] = "invalid_response"
                else:
                    return await self._async_create_bus_entry(user_input, stop_ids, payload)
            elif len(query) < 2:
                errors["base"] = "search_required"
            else:
                client = BusTimesApiClient(
                    async_get_clientsession(self.hass),
                    user_input[CONF_URL],
                )
                try:
                    results = await client.async_search_stops(query)
                except BusTimesConnectionError:
                    errors["base"] = "cannot_connect"
                except BusTimesInvalidResponseError:
                    errors["base"] = "invalid_response"
                else:
                    if not results:
                        errors["base"] = "no_stops_found"
                    else:
                        self._pending_url = user_input[CONF_URL].rstrip("/")
                        self._pending_interval = user_input[CONF_SCAN_INTERVAL]
                        self._search_results = results
                        return await self.async_step_select_stops()

        defaults = user_input or {}
        return self.async_show_form(
            step_id="user",
            data_schema=_schema(
                defaults.get(CONF_URL, DEFAULT_BASE_URL),
                defaults.get(CONF_STOP_QUERY, ""),
                _normalise_stop_ids(defaults.get(CONF_STOP_IDS, [])),
                defaults.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
            ),
            errors=errors,
            description_placeholders=description_placeholders,
        )

    async def async_step_select_stops(
        self,
        user_input: dict[str, Any] | None = None,
    ) -> ConfigFlowResult:
        """Allow one or more matching stops to be selected."""
        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = {}

        if user_input is not None:
            stop_ids = _normalise_stop_ids(user_input.get(CONF_STOP_IDS, []))
            validation_input = {
                CONF_URL: self._pending_url,
                CONF_STOP_IDS: stop_ids,
                CONF_SCAN_INTERVAL: self._pending_interval,
            }
            try:
                validated_ids, payload = await _validate_input(self.hass, validation_input)
            except BusTimesInvalidStopsError as err:
                errors["base"] = "invalid_stops"
                description_placeholders["invalid_stops"] = ", ".join(err.stop_ids) or "None selected"
            except BusTimesConnectionError:
                errors["base"] = "cannot_connect"
            except BusTimesInvalidResponseError:
                errors["base"] = "invalid_response"
            else:
                return await self._async_create_bus_entry(
                    validation_input,
                    validated_ids,
                    payload,
                )

        options = [
            selector.SelectOptionDict(
                value=result["id"],
                label=(
                    f'{result["name"]} — {result["description"]} ({result["id"]})'
                    if result["description"]
                    else f'{result["name"]} — {result["id"]}'
                ),
            )
            for result in self._search_results
        ]

        return self.async_show_form(
            step_id="select_stops",
            data_schema=vol.Schema(
                {
                    vol.Required(CONF_STOP_IDS): selector.SelectSelector(
                        selector.SelectSelectorConfig(
                            options=options,
                            multiple=True,
                            mode=selector.SelectSelectorMode.LIST,
                        )
                    )
                }
            ),
            errors=errors,
            description_placeholders=description_placeholders,
        )

    async def _async_create_bus_entry(
        self,
        user_input: dict[str, Any],
        stop_ids: list[str],
        payload: dict[str, Any],
    ) -> ConfigFlowResult:
        """Create the config entry after IDs have been validated."""
        await self.async_set_unique_id(user_input[CONF_URL].rstrip("/").lower())
        self._abort_if_unique_id_configured()
        names = [payload["stops"][stop_id]["stop"]["name"] for stop_id in stop_ids]
        return self.async_create_entry(
            title=f"Bus Times ({', '.join(names)})",
            data={
                CONF_URL: user_input[CONF_URL].rstrip("/"),
                CONF_STOP_IDS: stop_ids,
                CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
            },
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry: ConfigEntry) -> BusTimesOptionsFlow:
        return BusTimesOptionsFlow(config_entry)


class BusTimesOptionsFlow(OptionsFlow):
    """Allow stops and polling frequency to be changed in the UI."""

    def __init__(self, config_entry: ConfigEntry) -> None:
        self._entry = config_entry

    async def async_step_init(self, user_input: dict[str, Any] | None = None) -> ConfigFlowResult:
        errors: dict[str, str] = {}
        description_placeholders: dict[str, str] = {}
        current_stops = self._entry.options.get(CONF_STOP_IDS, self._entry.data[CONF_STOP_IDS])
        current_interval = self._entry.options.get(
            CONF_SCAN_INTERVAL,
            self._entry.data.get(CONF_SCAN_INTERVAL, DEFAULT_SCAN_INTERVAL),
        )

        if user_input is not None:
            validation_input = {CONF_URL: self._entry.data[CONF_URL], **user_input}
            try:
                stop_ids, _ = await _validate_input(self.hass, validation_input)
            except BusTimesInvalidStopsError as err:
                errors["base"] = "invalid_stops"
                description_placeholders["invalid_stops"] = ", ".join(err.stop_ids) or "None supplied"
            except BusTimesConnectionError:
                errors["base"] = "cannot_connect"
            except BusTimesInvalidResponseError:
                errors["base"] = "invalid_response"
            else:
                return self.async_create_entry(
                    title="",
                    data={
                        CONF_STOP_IDS: stop_ids,
                        CONF_SCAN_INTERVAL: user_input[CONF_SCAN_INTERVAL],
                    },
                )

        defaults = user_input or {}
        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema(
                {
                    vol.Required(
                        CONF_STOP_IDS,
                        default=defaults.get(CONF_STOP_IDS, ", ".join(current_stops)),
                    ): str,
                    vol.Required(
                        CONF_SCAN_INTERVAL,
                        default=defaults.get(CONF_SCAN_INTERVAL, current_interval),
                    ): vol.All(vol.Coerce(int), vol.Range(min=MIN_SCAN_INTERVAL, max=MAX_SCAN_INTERVAL)),
                }
            ),
            errors=errors,
            description_placeholders=description_placeholders,
        )
