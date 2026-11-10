# autobahn-mcp 🛣️

mcp-name: io.github.mohammad-abbasi-sh/autobahn-mcp

Unofficial **read-only** MCP server for **[verkehr.autobahn.de](https://verkehr.autobahn.de)** — German Autobahn data from the official verkehr.autobahn.de API: roadworks, closures, warnings, truck/car parking and EV charging stations per motorway. No key, no login.

> Built by Mohammad Abbasi as part of the "Germany MCP factory". Not affiliated with verkehr.autobahn.de.

## For AI agents

Add to your MCP client config (stdio):

```json
{
  "mcpServers": {
    "autobahn": {
      "command": "uvx",
      "args": ["autobahn-mcp==0.1.0"]
    }
  }
}
```

Or run locally: `python -m autobahn_mcp.server` (needs `mcp<2`, `httpx`).

## Tools

| Tool | Description |
|------|-------------|
| `autobahn_roadworks` | Roadworks on a motorway — `road` (e.g. "A1"), `limit` 1..50 |
| `autobahn_closures` | Closures on a motorway — `road` (e.g. "A1"), `limit` 1..50 |
| `autobahn_warnings` | Warnings on a motorway — `road` (e.g. "A100"), `limit` 1..50 |
| `autobahn_parking` | Truck/car parking on a motorway — `road` (e.g. "A1"), `limit` 1..50 |
| `autobahn_ev_charging` | EV charging stations on a motorway — `road` (e.g. "A1"), `limit` 1..50 |
| `autobahn_health` | Reachability probe (ok / blocked / error) — one polite request |

## Notes

- All data comes from the **official verkehr.autobahn.de API** (free, no key).
- The API's `reststop`, `traffic` and `webcam` services return empty arrays on every probed motorway right now (A1/A3/A7/A9/A100, verified 2026-11-10), so they are not exposed as tools; `parking_lorry` covers parking areas instead.
- Roadworks and closures can be numerous (A1 currently lists 261 roadworks) — use `limit` to cap the output.

Tests: 19/19 green (13 offline + 6 live, 2026-11-10).

## Development

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp<2" httpx pytest
.venv/bin/pip install -e .
.venv/bin/python -m pytest tests/ -q
```

## License

MIT

---

Built by [Mohammad Abbasi](https://github.com/mohammad-abbasi-sh) — [Almanibama](https://almanibama.ir) · [mabbasi.ir](https://mabbasi.ir)
