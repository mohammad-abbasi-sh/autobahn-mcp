# autobahn-mcp 🛣️

mcp-name: io.github.mohammad-abbasi-sh/autobahn-mcp

سرور MCP غیررسمی و **فقط‌خواندنی** برای **[verkehr.autobahn.de](https://verkehr.autobahn.de)** — داده‌های اتوبان آلمان از API رسمی verkehr.autobahn.de: کارهای جاده‌ای، بسته‌شدن‌ها، هشدارها، پارکینگ کامیون/خودرو و ایستگاه‌های شارژ خودروی برقی برای هر اتوبان. بدون کلید، بدون ورود.

> ساختهٔ محمد عباسی، بخشی از «کارخانهٔ MCP آلمان». وابسته به verkehr.autobahn.de نیست.

## برای ایجنت‌های هوش مصنوعی

به پیکربندی MCP کلاینت اضافه کنید (stdio):

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

یا به‌صورت محلی اجرا کنید: `python -m autobahn_mcp.server` (نیازمند `mcp<2` و `httpx`).

## ابزارها

| ابزار | توضیح |
|------|-------|
| `autobahn_roadworks` | کارهای جاده‌ای یک اتوبان |
| `autobahn_closures` | بسته‌شدن‌های یک اتوبان |
| `autobahn_warnings` | هشدارهای یک اتوبان |
| `autobahn_parking` | پارکینگ‌های یک اتوبان |
| `autobahn_ev_charging` | ایستگاه‌های شارژ خودروی برقی یک اتوبان |
| `autobahn_health` | بررسی دسترس‌پذیری (ok / blocked / error) — یک درخواست مؤدبانه |

## توسعه

```bash
python3 -m venv .venv && .venv/bin/pip install "mcp<2" httpx pytest
.venv/bin/pip install -e .
.venv/bin/python -m pytest tests/ -q
```

## لایسنس

MIT

---

Built by [Mohammad Abbasi](https://github.com/mohammad-abbasi-sh) — [Almanibama](https://almanibama.ir) · [mabbasi.ir](https://mabbasi.ir)
