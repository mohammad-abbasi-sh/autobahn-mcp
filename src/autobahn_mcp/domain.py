"""Domain logic: shape verkehr.autobahn.de API responses into compact
dicts (stdlib only).

Data source: the official Autobahn API
(https://verkehr.autobahn.de/o/autobahn/{road}/services/{service}) —
free, no key, no login. Services used: roadworks, closure, warning,
parking_lorry, electric_charging_station.

NOT exposed as tools (verified 2026-11-10): the `reststop` and
`traffic` services return empty arrays on A1/A3/A7/A9/A100 right now,
and `webcam` is empty on A1 — so they would only ever return nothing.
"""
from __future__ import annotations

import json
import re

BASE = "https://verkehr.autobahn.de/o/autobahn"

SERVICES = {
    "roadworks": "roadworks",
    "closure": "closure",
    "warning": "warning",
    "parking_lorry": "parking_lorry",
    "electric_charging_station": "electric_charging_station",
}

_ROAD_RE = re.compile(r"^A\d{1,3}$")


def validate_road(road: str) -> str:
    """Canonical motorway id, e.g. "A1" or "A100" (case-insensitive)."""
    key = (road or "").strip().upper()
    if not _ROAD_RE.match(key):
        raise ValueError(
            f"invalid road: {road!r} (expected a German motorway like \"A1\" or \"A100\")"
        )
    return key


def validate_limit(limit: int) -> int:
    if not 1 <= limit <= 50:
        raise ValueError(f"limit out of range: {limit} (expected 1..50)")
    return limit


def service_url(road: str, service: str) -> str:
    return f"{BASE}/{road}/services/{service}"


def _compact(item: dict) -> dict:
    desc = item.get("description") or []
    if isinstance(desc, list):
        desc = " | ".join(s.strip() for s in desc if (s or "").strip())
    coord = item.get("coordinate") or {}
    return {
        "identifier": item.get("identifier") or "",
        "title": item.get("title") or "",
        "subtitle": item.get("subtitle") or "",
        "description": desc,
        "display_type": item.get("display_type") or "",
        "is_blocked": item.get("isBlocked") == "true",
        "future": bool(item.get("future")),
        "start": item.get("startTimestamp") or "",
        "coordinate": (
            {"lat": coord.get("lat"), "long": coord.get("long")}
            if coord else None
        ),
    }


def parse_service(text: str, service: str) -> dict:
    """Parse one Autobahn service response into {count, items}.

    Empty arrays are valid — the API returns [] when a road currently
    has no entries of that kind.
    """
    key = SERVICES[service]
    try:
        data = json.loads(text)
    except json.JSONDecodeError as e:
        raise ValueError(f"invalid {service} response: {e}") from e
    items = data.get(key)
    if items is None:
        raise ValueError(f"unexpected {service} shape: no {key!r} list")
    if not isinstance(items, list):
        raise ValueError(f"unexpected {service} shape: {key!r} is not a list")
    return {"count": len(items), "items": [_compact(it) for it in items]}
