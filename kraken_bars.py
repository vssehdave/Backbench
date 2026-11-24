"""Kraken public OHLC daily bars (UTC, 24/7) as (date, open, close) rows."""
import hashlib
import json
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

URL = "https://api.kraken.com/0/public/OHLC"
DAY = 86400


def _get(url, retries=3):
    """GET JSON; Kraken sends HTTP 200 with a non-empty 'error' list on failure."""
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(url, timeout=60) as reply:
                body = json.load(reply)
        except urllib.error.HTTPError as exc:
            if exc.code not in (429, 502, 503) or attempt == retries:
                raise RuntimeError(f"Kraken request failed (HTTP {exc.code})") from None
            time.sleep(2 ** attempt)
            continue
        if any("EAPI:Rate limit" in e for e in body.get("error", [])) and attempt < retries:
            time.sleep(2 ** attempt)
            continue
        if body.get("error"):
            raise RuntimeError(f"Kraken error: {body['error']}")
        return body


def _digest(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def fetch(pair, data_dir=Path("data/kraken")):
    """Raw OHLC response, cached per pair and UTC fetch date with provenance. Kraken serves only ~720 recent days."""
    pair = pair.upper()
    cache = Path(data_dir) / f"{pair}_{datetime.now(timezone.utc).date()}_raw.json"
    if cache.is_file():
        return json.loads(cache.read_text(encoding="utf-8"))
    params = {"pair": pair, "interval": 1440}
    response = _get(f"{URL}?{urllib.parse.urlencode(params)}")
    record = {"provenance": {"source": "kraken", "url": URL, "params": params,
                             "fetched_at_utc": datetime.now(timezone.utc).isoformat(),
                             "response_sha256": _digest(response)},
              "response": response}
    cache.parent.mkdir(parents=True, exist_ok=True)
    temporary = cache.with_suffix(".tmp")
    temporary.write_text(json.dumps(record), encoding="utf-8")
    temporary.replace(cache)
    return record


def daily_from_kraken(pair, data_dir=Path("data/kraken"), allow_gaps=False):
    record = fetch(pair, data_dir)
    if _digest(record["response"]) != record["provenance"]["response_sha256"]:
        raise ValueError("Cached Kraken payload does not match its recorded sha256")
    series = [v for k, v in record["response"]["result"].items() if k != "last"]
    if len(series) != 1 or not series[0]:
        raise ValueError(f"Kraken returned no single candle series for {pair}")
    fetched = datetime.fromisoformat(record["provenance"]["fetched_at_utc"]).timestamp()
    rows = {}
    for candle in series[0]:
        opened = int(candle[0])
        # A candle opened less than a day before the fetch is still forming.
        if opened % DAY or opened + DAY > fetched:
            if opened % DAY:
                raise ValueError(f"Kraken candle at {opened} is not aligned to a UTC day")
            continue
        op, close = float(candle[1]), float(candle[4])
        if not (op > 0 and close > 0):
            raise ValueError(f"Unusable open or close at {opened}")
        day = datetime.fromtimestamp(opened, timezone.utc).date()
        rows[day] = (day, op, close)
    if not rows:
        raise ValueError("Kraken returned no completed daily candles")
    first, last = min(rows), max(rows)
    missing = [first + timedelta(days=i) for i in range((last - first).days + 1) if first + timedelta(days=i) not in rows]
    if missing and not allow_gaps:
        raise ValueError("Kraken daily bars have missing UTC dates: " + ", ".join(map(str, missing)))
    return [rows[d] for d in sorted(rows)], {
        "resolution": "Kraken OHLC interval=1440, UTC days; the still-open current candle is dropped",
        "pair": pair.upper(),
        "response_sha256": record["provenance"]["response_sha256"],
        "fetched_at_utc": record["provenance"]["fetched_at_utc"],
        "session_count": len(rows),
        "missing_dates": [str(d) for d in missing],
        "first_date": str(first),
        "last_date": str(last),
        "weekend_sessions": sum(d.weekday() >= 5 for d in rows),
    }
