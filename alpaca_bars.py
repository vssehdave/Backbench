"""Alpaca Market Data v2 one-minute bars as as-traded regular-hours daily bars."""
import hashlib
import json
import math
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

DATA = "https://data.alpaca.markets"
EASTERN = ZoneInfo("America/New_York")
SPLITS = ("forward_splits", "reverse_splits", "unit_splits")
ACTION_TYPES = "forward_split,reverse_split,unit_split,cash_dividend,stock_dividend"
ROOT = Path(__file__).resolve().parent


class SplitInRange(ValueError):
    pass


def _env(env_file=ROOT / ".env"):
    values = {k: v for k, v in os.environ.items() if k.startswith("APCA_") and v}
    if Path(env_file).is_file():
        for line in Path(env_file).read_text(encoding="utf-8-sig").splitlines():
            name, sep, value = line.strip().partition("=")
            if sep and name.startswith("APCA_") and name not in values and value.strip().strip("\"'"):
                values[name] = value.strip().strip("\"'")
    return values


def credentials(env_file=ROOT / ".env"):
    values = _env(env_file)
    if not {"APCA_API_KEY_ID", "APCA_API_SECRET_KEY"} <= values.keys():
        raise RuntimeError("Set APCA_API_KEY_ID and APCA_API_SECRET_KEY in the environment or .env")
    return {"APCA-API-KEY-ID": values["APCA_API_KEY_ID"], "APCA-API-SECRET-KEY": values["APCA_API_SECRET_KEY"]}


def _get(url, headers, retries=5):
    """GET JSON. Backs off on 429 and never echoes headers."""
    for attempt in range(retries + 1):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=60) as reply:
                return json.load(reply)
        except urllib.error.HTTPError as exc:
            if exc.code in (401, 403):
                raise RuntimeError(f"Alpaca refused the request (HTTP {exc.code}). Check the keys; the free "
                                   "plan may restrict recent SIP data, so use an older --end or an IEX feed.") from None
            if exc.code != 429 or attempt == retries:
                raise RuntimeError(f"Alpaca request failed (HTTP {exc.code})") from None
            time.sleep(min(30, float(exc.headers.get("Retry-After") or 2 ** attempt)))


def _pages(path, params, headers):
    """Return every raw response page, following next_page_token."""
    pages, token = [], None
    while True:
        query = dict(params, **({"page_token": token} if token else {}))
        page = _get(f"{DATA}{path}?{urllib.parse.urlencode(query)}", headers)
        pages.append(page)
        token = page.get("next_page_token")
        if not token:
            return pages


def _digest(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _calendar(start, end, headers):
    base = _env().get("APCA_API_BASE_URL", "https://paper-api.alpaca.markets/v2").rstrip("/")
    query = urllib.parse.urlencode({"start": str(start), "end": str(end - timedelta(days=1))})
    return _get(f"{base}/calendar?{query}", headers)


def fetch(symbol, start, end, feed="sip", data_dir=Path("data/alpaca")):
    """Raw bar, corporate-action and trading-calendar payloads for [start, end), cached with provenance."""
    cache = Path(data_dir) / f"{symbol.upper()}_{start}_{end}_{feed}_raw.json"
    record = json.loads(cache.read_text(encoding="utf-8")) if cache.is_file() else None
    if record and "calendar" in record["pages"]:
        return record
    headers = credentials()
    if record is None:
        last = end - timedelta(days=1)
        bar_params = {"timeframe": "1Min", "adjustment": "raw", "feed": feed, "limit": 10000, "sort": "asc",
                      "start": f"{start}T00:00:00Z", "end": f"{end}T00:00:00Z"}
        action_params = {"symbols": symbol.upper(), "types": ACTION_TYPES, "start": str(start), "end": str(last),
                         "limit": 1000}
        record = {"provenance": {"source": "alpaca", "feed": feed, "adjustment": "raw", "symbol": symbol.upper(),
                                 "bars_request": bar_params, "corporate_actions_request": action_params,
                                 "fetched_at_utc": datetime.now(timezone.utc).isoformat()},
                  "pages": {"bars": _pages(f"/v2/stocks/{symbol.upper()}/bars", bar_params, headers),
                            "corporate_actions": _pages("/v1/corporate-actions", action_params, headers)}}
    # Caches written before the calendar existed are completed here rather than refetched.
    record["pages"]["calendar"] = _calendar(start, end, headers)
    record["provenance"]["calendar_request"] = {"start": str(start), "end": str(end - timedelta(days=1))}
    record["provenance"]["pages_sha256"] = _digest(record["pages"])
    cache.parent.mkdir(parents=True, exist_ok=True)
    temporary = cache.with_suffix(".tmp")
    temporary.write_text(json.dumps(record), encoding="utf-8")
    temporary.replace(cache)
    return record


def _bars(page, symbol):
    bars = page.get("bars") or []
    return bars.get(symbol, []) if isinstance(bars, dict) else bars


def daily_from_alpaca(symbol, start, end, feed="sip", data_dir=Path("data/alpaca"), allow_splits=False):
    symbol = symbol.upper()
    record = fetch(symbol, start, end, feed, data_dir)
    if _digest(record["pages"]) != record["provenance"]["pages_sha256"]:
        raise ValueError("Cached Alpaca payload does not match its recorded sha256")
    actions = {}
    for page in record["pages"]["corporate_actions"]:
        for kind, items in (page.get("corporate_actions") or {}).items():
            actions.setdefault(kind, []).extend(items)
    splits = [dict(a, type=k) for k in SPLITS for a in actions.get(k, [])]
    if splits and not allow_splits:
        raise SplitInRange(f"{symbol} has splits in {start}..{end}: "
                           + ", ".join(f"{s['type']} {s.get('ex_date') or s.get('effective_date')}" for s in splits)
                           + ". As-traded prices break across splits; pass --allow-splits to accept this.")
    sessions = {}
    for entry in record["pages"]["calendar"]:
        (oh, om), (ch, cm) = (map(int, entry[k].split(":")) for k in ("open", "close"))
        sessions[date.fromisoformat(entry["date"])] = (oh * 60 + om, ch * 60 + cm)
    bars, counts, previous = [], [], None
    for page in record["pages"]["bars"]:
        for raw in _bars(page, symbol):
            moment = datetime.fromisoformat(raw["t"].replace("Z", "+00:00")).astimezone(EASTERN)
            minute = moment.hour * 60 + moment.minute
            day = moment.date()
            if not start <= day < end or not 570 <= minute < 960:
                continue
            if day not in sessions:
                raise ValueError(f"Regular-hours bar on {day}, which is not in Alpaca's trading calendar")
            if not sessions[day][0] <= minute < sessions[day][1]:
                continue
            if previous and (day, minute) <= previous:
                raise ValueError(f"Duplicate or unordered minute at {raw['t']}")
            op, close = float(raw["o"]), float(raw["c"])
            if not all(math.isfinite(x) and x > 0 for x in (op, close)):
                raise ValueError(f"Unusable open or close at {raw['t']}")
            if not previous or day != previous[0]:
                bars.append((day, op, close))
                counts.append([day.isoformat(), minute, minute, 1])
            else:
                bars[-1] = (day, bars[-1][1], close)
                counts[-1][2] = minute
                counts[-1][3] += 1
            previous = (day, minute)
    missing = sorted(set(sessions) - {b[0] for b in bars})
    if missing:
        raise ValueError(f"No regular-hours bars for calendar sessions: {', '.join(map(str, missing))}")
    return bars, {
        "resolution": "daily from observed Eastern minute bars within each calendar session",
        "symbol_source": "user supplied",
        "feed": feed,
        "adjustment": "raw",
        "pages_sha256": record["provenance"]["pages_sha256"],
        "fetched_at_utc": record["provenance"]["fetched_at_utc"],
        "session_count": len(bars),
        "early_closes": [{"date": d.isoformat(), "close_minute": c} for d, (_, c) in sorted(sessions.items())
                         if c != 960],
        "sessions_short_of_calendar": [
            {"date": d, "first_minute": first, "last_minute": last, "observations": n,
             "expected": sessions[date.fromisoformat(d)][1] - sessions[date.fromisoformat(d)][0]}
            for d, first, last, n in counts
            if n < sessions[date.fromisoformat(d)][1] - sessions[date.fromisoformat(d)][0]
        ],
        "splits": splits,
        "splits_allowed": bool(splits),
        "cash_dividends": actions.get("cash_dividends", []),
        "stock_dividends": actions.get("stock_dividends", []),
    }
