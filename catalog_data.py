"""Daily OHLCV for the catalog runs: Alpaca (split and dividend adjusted, SIP) and Kraken BTC. Cached under data/."""
import json
import urllib.parse
from datetime import datetime, timezone, date
from pathlib import Path

import alpaca_bars
import kraken_bars


def alpaca_daily(symbol, start, end, data_dir=Path("data/alpaca_daily")):
    """Rows (day, open, high, low, close, volume), adjustment=all, for start <= day < end."""
    symbol = symbol.upper()
    cache = Path(data_dir) / f"{symbol}_{start}_{end}_sip_all.json"
    if cache.is_file():
        pages = json.loads(cache.read_text(encoding="utf-8"))
    else:
        params = {"timeframe": "1Day", "adjustment": "all", "feed": "sip", "limit": 10000, "sort": "asc",
                  "start": f"{start}T00:00:00Z", "end": f"{end}T00:00:00Z"}
        pages = alpaca_bars._pages(f"/v2/stocks/{symbol}/bars", params, alpaca_bars.credentials())
        cache.parent.mkdir(parents=True, exist_ok=True)
        cache.write_text(json.dumps(pages), encoding="utf-8")
    rows = {}
    for page in pages:
        for b in alpaca_bars._bars(page, symbol):
            day = date.fromisoformat(b["t"][:10])
            row = (day, float(b["o"]), float(b["h"]), float(b["l"]), float(b["c"]), float(b["v"]))
            if not all(x > 0 for x in row[1:5]) or not row[2] >= max(row[1], row[4]) >= min(row[1], row[4]) >= row[3]:
                raise ValueError(f"{symbol} {day}: inconsistent OHLC {row[1:5]}")
            rows[day] = row
    if not rows:
        raise ValueError(f"No Alpaca daily bars for {symbol} in {start}..{end}")
    return [rows[d] for d in sorted(rows)]


def kraken_daily(pair="XBTUSD"):
    """Completed UTC-day candles as (day, open, high, low, close, volume). Kraken serves about 720 days."""
    record = kraken_bars.fetch(pair)
    series = [v for k, v in record["response"]["result"].items() if k != "last"][0]
    fetched = datetime.fromisoformat(record["provenance"]["fetched_at_utc"]).timestamp()
    rows = []
    for c in series:
        t = int(c[0])
        if t % kraken_bars.DAY or t + kraken_bars.DAY > fetched:
            continue
        rows.append((datetime.fromtimestamp(t, timezone.utc).date(), *(float(x) for x in (c[1], c[2], c[3], c[4], c[6]))))
    return rows
