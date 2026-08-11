"""API client for Brighton Bus Times."""

from __future__ import annotations

import asyncio
from typing import Any

from aiohttp import ClientError, ClientSession

from .const import API_PATH, STOPS_PATH


class BusTimesApiError(Exception):
    """Base API error."""


class BusTimesConnectionError(BusTimesApiError):
    """Raised when the API cannot be reached."""


class BusTimesInvalidResponseError(BusTimesApiError):
    """Raised when the API response is malformed."""


class BusTimesInvalidStopsError(BusTimesApiError):
    """Raised when one or more stops do not exist."""

    def __init__(self, stop_ids: list[str]) -> None:
        self.stop_ids = stop_ids
        super().__init__(", ".join(stop_ids))


class BusTimesApiClient:
    """Small async client for the Home Assistant departures endpoint."""

    def __init__(self, session: ClientSession, base_url: str) -> None:
        self._session = session
        self._base_url = base_url.rstrip("/")

    async def async_get_departures(self, stop_ids: list[str]) -> dict[str, Any]:
        """Fetch departures for all configured stops in one request."""
        url = f"{self._base_url}{API_PATH}"

        try:
            async with asyncio.timeout(20):
                response = await self._session.get(
                    url,
                    params={"stops": ",".join(stop_ids)},
                )
                response.raise_for_status()
                payload = await response.json(content_type=None)
        except (TimeoutError, ClientError, ValueError) as err:
            raise BusTimesConnectionError from err

        if not isinstance(payload, dict) or payload.get("success") is not True:
            raise BusTimesInvalidResponseError

        stops = payload.get("stops")
        if not isinstance(stops, dict):
            raise BusTimesInvalidResponseError

        errors = payload.get("errors", {})
        if errors is not None and not isinstance(errors, (dict, list)):
            raise BusTimesInvalidResponseError

        return payload

    async def async_search_stops(self, query: str, limit: int = 30) -> list[dict[str, str]]:
        """Search the same generated stop data used by the public map."""
        url = f"{self._base_url}{STOPS_PATH}"

        try:
            async with asyncio.timeout(20):
                response = await self._session.get(url)
                response.raise_for_status()
                payload = await response.json(content_type=None)
        except (TimeoutError, ClientError, ValueError) as err:
            raise BusTimesConnectionError from err

        features = payload.get("features") if isinstance(payload, dict) else None
        if not isinstance(features, list):
            raise BusTimesInvalidResponseError

        wanted = query.strip().casefold()
        if len(wanted) < 2:
            return []

        matches: list[tuple[int, str, dict[str, str]]] = []
        for feature in features:
            if not isinstance(feature, dict):
                continue
            properties = feature.get("properties")
            if not isinstance(properties, dict):
                continue

            stop_id = str(properties.get("id") or feature.get("id") or "").strip()
            name = str(properties.get("name") or "").strip()
            code = str(properties.get("code") or "").strip()
            description = str(properties.get("description") or "").strip()
            haystack = f"{name} {code} {stop_id} {description}".casefold()
            if not stop_id or wanted not in haystack:
                continue

            folded_name = name.casefold()
            score = 0 if folded_name == wanted else 1 if folded_name.startswith(wanted) else 2
            matches.append(
                (
                    score,
                    name.casefold(),
                    {
                        "id": stop_id,
                        "name": name or f"Stop {stop_id}",
                        "code": code,
                        "description": description,
                    },
                )
            )

        matches.sort(key=lambda item: (item[0], item[1], item[2]["id"]))
        return [item[2] for item in matches[:limit]]

    async def async_validate_stops(self, stop_ids: list[str]) -> dict[str, Any]:
        """Validate all stop IDs and return the initial response."""
        payload = await self.async_get_departures(stop_ids)
        invalid = [
            stop_id
            for stop_id in stop_ids
            if stop_id not in payload["stops"] or stop_id in payload.get("errors", {})
        ]
        if invalid:
            raise BusTimesInvalidStopsError(invalid)
        return payload
