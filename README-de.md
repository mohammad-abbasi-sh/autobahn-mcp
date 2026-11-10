# autobahn-mcp 🛣️

mcp-name: io.github.mohammad-abbasi-sh/autobahn-mcp

Inoffizieller **nur lesender** MCP-Server für **[verkehr.autobahn.de](https://verkehr.autobahn.de)** — Deutsche Autobahn-Daten über die offizielle API verkehr.autobahn.de: Baustellen, Sperrungen, Warnungen, LKW-/PKW-Parkplätze und E-Ladesäulen je Autobahn. Kein Schlüssel, keine Anmeldung.

> Gebaut von Mohammad Abbasi als Teil der "Germany MCP factory". Nicht mit verkehr.autobahn.de verbunden.

## Für KI-Agenten

Zur MCP-Client-Konfiguration hinzufügen (stdio):

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

Oder lokal starten: `python -m autobahn_mcp.server` (benötigt `mcp<2`, `httpx`).

## Tools

| Tool | Beschreibung |
|------|-------------|
| `autobahn_roadworks` | Baustellen auf einer Autobahn |
| `autobahn_closures` | Sperrungen auf einer Autobahn |
| `autobahn_warnings` | Warnungen auf einer Autobahn |
| `autobahn_parking` | Parkplätze auf einer Autobahn |
| `autobahn_ev_charging` | E-Ladesäulen auf einer Autobahn |
| `autobahn_health` | Erreichbarkeitsprüfung (ok / blocked / error) — eine höfliche Anfrage |

## Entwicklung

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp<2" httpx pytest
.venv/bin/pip install -e .
.venv/bin/python -m pytest tests/ -q
```

## Lizenz

MIT

---

Built by [Mohammad Abbasi](https://github.com/mohammad-abbasi-sh) — [Almanibama](https://almanibama.ir) · [mabbasi.ir](https://mabbasi.ir)
