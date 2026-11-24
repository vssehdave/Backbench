"""Alpaca historical option contracts and daily option bars, cached raw with a sha256 like alpaca_bars."""
import json
import urllib.parse
from datetime import datetime, timedelta, timezone
from pathlib import Path

import alpaca_bars as ab


def _cached(path, provenance, pages_fn):
    """Return the pages for one request, fetching once and re-verifying the stored sha256 on every load."""
    path = Path(path)
    if path.is_file():
        record = json.loads(path.read_text(encoding="utf-8"))
        if ab._digest(record["pages"]) != record["provenance"]["pages_sha256"]:
            raise ValueError(f"Cached payload {path} does not match its recorded sha256")
        return record["pages"]
    pages = pages_fn(ab.credentials())
    provenance = dict(provenance, source="alpaca", fetched_at_utc=datetime.now(timezone.utc).isoformat(),
                      pages_sha256=ab._digest(pages))
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps({"provenance": provenance, "pages": pages}), encoding="utf-8")
    temporary.replace(path)
    return pages


def contracts(underlying, expiry, kind, low, high, today, data_dir=Path("data/alpaca_options")):
    """{strike: OCC symbol} for one expiry and type with strikes in [low, high].

    Expired contracts are only listed under status=inactive; status=expired silently returns nothing.
    """
    params = {"underlying_symbols": underlying, "expiration_date": str(expiry), "type": kind,
              "status": "inactive" if expiry < today else "active", "limit": 10000,
              "strike_price_gte": f"{low:.0f}", "strike_price_lte": f"{high:.0f}"}

    def fetch(headers):
        base = ab._env().get("APCA_API_BASE_URL", "https://paper-api.alpaca.markets/v2").rstrip("/")
        pages, token = [], None
        while True:
            query = urllib.parse.urlencode(dict(params, **({"page_token": token} if token else {})))
            pages.append(ab._get(f"{base}/options/contracts?{query}", headers))
            token = pages[-1].get("next_page_token")
            if not token:
                return pages

    path = Path(data_dir) / f"contracts_{underlying}_{expiry}_{kind}_{params['strike_price_gte']}_{params['strike_price_lte']}.json"
    pages = _cached(path, {"request": params}, fetch)
    return {float(c["strike_price"]): c["symbol"] for p in pages for c in p.get("option_contracts") or []}


def option_closes(symbol, start, end, data_dir=Path("data/alpaca_options")):
    """{date: close} of daily option bars in [start, end]. These are trade prices, not quotes; no-trade days have no bar."""
    params = {"symbols": symbol, "timeframe": "1Day", "limit": 1000, "sort": "asc",
              "start": f"{start}T00:00:00Z", "end": f"{end + timedelta(days=1)}T00:00:00Z"}
    pages = _cached(Path(data_dir) / f"bars_{symbol}_{start}_{end}.json", {"request": params},
                    lambda headers: ab._pages("/v1beta1/options/bars", params, headers))
    rows = [bar for p in pages for bar in (p.get("bars") or {}).get(symbol, [])]
    return {datetime.fromisoformat(b["t"].replace("Z", "+00:00")).astimezone(ab.EASTERN).date(): float(b["c"])
            for b in rows}


def underlying_closes(symbol, start, end, feed="sip", data_dir=Path("data/alpaca_options")):
    """{date: raw close} of daily stock bars in [start, end]. Price only: dividends are not included."""
    params = {"timeframe": "1Day", "adjustment": "raw", "feed": feed, "limit": 1000, "sort": "asc",
              "start": f"{start}T00:00:00Z", "end": f"{end + timedelta(days=1)}T00:00:00Z"}
    pages = _cached(Path(data_dir) / f"{symbol}_{start}_{end}_{feed}_daily.json", {"request": params},
                    lambda headers: ab._pages(f"/v2/stocks/{symbol}/bars", params, headers))
    return {datetime.fromisoformat(b["t"].replace("Z", "+00:00")).astimezone(ab.EASTERN).date(): float(b["c"])
            for p in pages for b in p.get("bars") or []}
