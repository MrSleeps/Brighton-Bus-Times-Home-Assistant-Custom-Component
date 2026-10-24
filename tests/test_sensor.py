"""Regression tests for the bus stop Recorder attribute exclusions."""

from __future__ import annotations

import json
from unittest.mock import Mock

from custom_components.brighton_bus_times.sensor import BusStopDepartureSensor


def test_large_departure_board_is_live_but_not_recorded() -> None:
    """Keep the full board available without exceeding Recorder's 16 KiB limit."""
    stop_id = "149000006952"
    departures = [
        {
            "route": "2",
            "destination": "Rottingdean",
            "eta_minutes": index,
            "eta_display": f"{index} min",
            "status": "live",
            "is_live": True,
            "extra_information": "x" * 300,
        }
        for index in range(100)
    ]
    routes = [{"route": str(index), "name": "Route " + str(index)} for index in range(100)]
    coordinator = Mock()
    coordinator.last_update_success = True
    coordinator.data = {
        "stops": {
            stop_id: {
                "stop": {"name": "Second Avenue (opp)"},
                "departures": departures,
                "routes_serving_stop": routes,
            }
        }
    }

    sensor = BusStopDepartureSensor(coordinator, stop_id)
    attributes = sensor.extra_state_attributes

    assert sensor.native_value == 0
    assert attributes["departures"] is departures
    assert attributes["routes_serving_stop"] is routes

    # Recorder uses this *class* attribute, without removing it from live state.
    excluded = BusStopDepartureSensor._unrecorded_attributes
    assert isinstance(excluded, frozenset)
    assert {"departures", "routes_serving_stop"} <= excluded

    recorded_attributes = {
        key: value for key, value in attributes.items() if key not in excluded
    }
    assert len(json.dumps(attributes).encode("utf-8")) > 16_384
    assert len(json.dumps(recorded_attributes).encode("utf-8")) < 16_384
    assert recorded_attributes["stop_id"] == stop_id
    assert recorded_attributes["route"] == "2"
