"""Sensors for Brighton Bus Times."""

from __future__ import annotations

from typing import Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import UnitOfTime
from homeassistant.core import HomeAssistant
from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEFAULT_BASE_URL, DOMAIN
from .coordinator import BusTimesDataUpdateCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    coordinator: BusTimesDataUpdateCoordinator = entry.runtime_data
    async_add_entities(BusStopDepartureSensor(coordinator, stop_id) for stop_id in coordinator.stop_ids)


class BusStopDepartureSensor(CoordinatorEntity[BusTimesDataUpdateCoordinator], SensorEntity):
    """Next departure and full departure board for one stop."""

    _attr_has_entity_name = True
    _attr_name = "Next departure"
    _attr_icon = "mdi:bus-clock"
    _attr_native_unit_of_measurement = UnitOfTime.MINUTES

    # Departure board data remains available to dashboards and automations, but
    # these potentially large lists must not be stored in Recorder history.
    _unrecorded_attributes = frozenset({"departures", "routes_serving_stop"})

    def __init__(self, coordinator: BusTimesDataUpdateCoordinator, stop_id: str) -> None:
        super().__init__(coordinator)
        self._stop_id = stop_id
        self._attr_unique_id = f"{stop_id}_next_departure"

    @property
    def _stop_data(self) -> dict[str, Any] | None:
        return self.coordinator.data.get("stops", {}).get(self._stop_id)

    @property
    def available(self) -> bool:
        return super().available and self._stop_data is not None

    @property
    def device_info(self) -> DeviceInfo:
        stop = (self._stop_data or {}).get("stop", {})
        return DeviceInfo(
            identifiers={(DOMAIN, self._stop_id)},
            name=stop.get("name", f"Bus stop {self._stop_id}"),
            manufacturer="Brighton Bus Times",
            model="Bus stop",
            configuration_url=f"{DEFAULT_BASE_URL}/bus/stop/{self._stop_id}",
        )

    @property
    def native_value(self) -> int | None:
        departures = (self._stop_data or {}).get("departures", [])
        if not departures:
            return None
        return departures[0].get("eta_minutes")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        stop_data = self._stop_data or {}
        stop = stop_data.get("stop", {})
        departures = stop_data.get("departures", [])
        next_departure = departures[0] if departures else {}

        return {
            "stop_id": self._stop_id,
            "stop_name": stop.get("name"),
            "latitude": stop.get("latitude"),
            "longitude": stop.get("longitude"),
            "route": next_departure.get("route"),
            "destination": next_departure.get("destination"),
            "eta_display": next_departure.get("eta_display"),
            "status": next_departure.get("status"),
            "status_display": next_departure.get("status_display"),
            "is_live": next_departure.get("is_live"),
            "direction": next_departure.get("direction"),
            "scheduled_departure": next_departure.get("scheduled_departure"),
            "vehicle_ref": next_departure.get("vehicle_ref"),
            "distance": next_departure.get("distance"),
            "departures": departures,
            "routes_serving_stop": stop_data.get("routes_serving_stop", []),
            "last_updated": stop_data.get("last_updated"),
            "live_cache_status": stop_data.get("live_cache_status"),
            "live_cache_age_seconds": stop_data.get("live_cache_age_seconds"),
            "source": stop_data.get("source"),
        }
