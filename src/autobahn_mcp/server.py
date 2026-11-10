"""MCP server: unofficial read-only access to the German Autobahn —
roadworks, closures, warnings, parking and EV charging — via the
official verkehr.autobahn.de API. No key, no login."""
from __future__ import annotations

import json
import sys
from datetime import datetime, timezone

from mcp.server.fastmcp import FastMCP

from . import domain as _dom
from . import http as _http

INSTRUCTIONS = """\
Unofficial read-only MCP server for the German Autobahn via the \
official verkehr.autobahn.de API (no key, no login): roadworks, \
closures, warnings, truck/car parking areas and EV charging stations \
for one motorway at a time (e.g. "A1", "A100"). NOTE: the API's \
`reststop`, `traffic` and `webcam` services return empty arrays on \
every probed motorway right now (verified 2026-11-10), so they are \
not exposed as tools. Built by Mohammad Abbasi (mohammad-abbasi-sh) \
— https://almanibama.ir · https://mabbasi.ir — Germany MCP factory.\
"""

_SOURCE = "verkehr.autobahn.de"
_DISCLAIMER = "Unofficial read-only data from verkehr.autobahn.de; verify on the site before acting on it."


def _envelope() -> dict:
    return {
        "fetched_at": datetime.now(timezone.utc).isoformat(),
        "source": _SOURCE,
        "disclaimer": _DISCLAIMER,
    }


def _ok(payload: dict) -> str:
    return json.dumps({**_envelope(), **payload}, ensure_ascii=False)


def _err(e: Exception) -> str:
    return _ok({"error": str(e)})


mcp = FastMCP("autobahn-mcp", instructions=INSTRUCTIONS)


def _service(road: str, service: str, limit: int) -> dict:
    r = _dom.validate_road(road)
    lim = _dom.validate_limit(limit)
    parsed = _dom.parse_service(_http.fetch_text(_dom.service_url(r, service)), service)
    return {"road": r, "total_results": parsed["count"],
            "count": min(lim, parsed["count"]), "items": parsed["items"][:lim]}


@mcp.tool()
def autobahn_roadworks(road: str = "A1", limit: int = 10) -> str:
    """Roadworks on one German motorway. road: e.g. "A1" or "A100".
    limit: 1..50 (default 10)."""
    try:
        out = _service(road, "roadworks", limit)
    except (_http.AutobahnMcpError, ValueError) as e:
        return _err(e)
    return _ok(out)


@mcp.tool()
def autobahn_closures(road: str = "A1", limit: int = 10) -> str:
    """Closures on one German motorway. road: e.g. "A1" or "A100".
    limit: 1..50 (default 10)."""
    try:
        out = _service(road, "closure", limit)
    except (_http.AutobahnMcpError, ValueError) as e:
        return _err(e)
    return _ok(out)


@mcp.tool()
def autobahn_warnings(road: str = "A100", limit: int = 10) -> str:
    """Warnings on one German motorway. road: e.g. "A100" or "A1".
    limit: 1..50 (default 10)."""
    try:
        out = _service(road, "warning", limit)
    except (_http.AutobahnMcpError, ValueError) as e:
        return _err(e)
    return _ok(out)


@mcp.tool()
def autobahn_parking(road: str = "A1", limit: int = 10) -> str:
    """Truck/car parking areas on one German motorway, with capacities.
    road: e.g. "A1" or "A7". limit: 1..50 (default 10)."""
    try:
        out = _service(road, "parking_lorry", limit)
    except (_http.AutobahnMcpError, ValueError) as e:
        return _err(e)
    return _ok(out)


@mcp.tool()
def autobahn_ev_charging(road: str = "A1", limit: int = 10) -> str:
    """EV charging stations on one German motorway.
    road: e.g. "A1" or "A7". limit: 1..50 (default 10)."""
    try:
        out = _service(road, "electric_charging_station", limit)
    except (_http.AutobahnMcpError, ValueError) as e:
        return _err(e)
    return _ok(out)


@mcp.tool()
def autobahn_health() -> str:
    """Check whether verkehr.autobahn.de is reachable right now.

    Returns status ok (HTTP 200), blocked (HTTP 403/429 — bot wall or
    rate limit) or error, plus the HTTP status and the probed URL.
    One polite request; it does not fetch any listings."""
    return _ok(_http.health_check())


def main() -> None:
    mcp.run()


if __name__ == "__main__":
    sys.exit(main())
