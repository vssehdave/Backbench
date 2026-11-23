"""Resume historical Massive U.S. equity trade and quote downloads by ticker."""
import argparse
import gzip
import hashlib
import json
import os
import re
import sqlite3
import sys
import time
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener


API = "https://api.massive.com"
KINDS = ("trades", "quotes")
DAY_NS = 86_400_000_000_000


class NoRedirect(HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def request_json(url, key):
    request = Request(url, headers={"Authorization": "Bearer " + key})
    opener = build_opener(NoRedirect)
    for attempt in range(5):
        try:
            with opener.open(request, timeout=45) as response:
                return json.load(response)
        except HTTPError as error:
            with error:
                if error.code not in {429, 500, 502, 503, 504} or attempt == 4:
                    raise RuntimeError(f"Massive returned HTTP {error.code}; verify entitlement and connectivity") from None
                retry = error.headers.get("Retry-After", "")
                delay = int(retry) if retry.isdigit() else 2 ** attempt
                if delay > 60:
                    raise RuntimeError("Rate-limit cooldown exceeds one minute; resume later") from None
        except (TimeoutError, URLError):
            if attempt == 4:
                raise RuntimeError("Massive connection failed after five attempts") from None
            delay = 2 ** attempt
        time.sleep(delay)


def database(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    db = sqlite3.connect(path, timeout=60)
    db.executescript("""
        CREATE TABLE IF NOT EXISTS partitions (
            symbol TEXT, kind TEXT, day TEXT, next_url TEXT, pages INTEGER DEFAULT 0,
            records INTEGER DEFAULT 0, PRIMARY KEY (symbol, kind, day)
        );
        CREATE TABLE IF NOT EXISTS pages (
            symbol TEXT, kind TEXT, day TEXT, page INTEGER, source_url TEXT,
            request_id TEXT, received_utc TEXT, sha256 TEXT, payload BLOB,
            PRIMARY KEY (symbol, kind, day, page), UNIQUE (symbol, kind, day, source_url)
        );
    """)
    return db


def safe_url(url, path):
    parsed = urlsplit(url)
    if (parsed.scheme, parsed.netloc, parsed.path, parsed.fragment) != ("https", "api.massive.com", path, ""):
        raise ValueError("Unexpected pagination endpoint")
    query = [(k, v) for k, v in parse_qsl(parsed.query, keep_blank_values=True)
             if k.lower() != "apikey"]
    return urlunsplit(parsed._replace(query=urlencode(query)))


def download_day(db, symbol, kind, day, fetch):
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9.\-]{0,31}", symbol) or kind not in KINDS:
        raise ValueError("Unsupported ticker or feed")
    key = (symbol, kind, day.isoformat())
    path = f"/v3/{kind}/{symbol}"
    start = (day - date(1970, 1, 1)).days * DAY_NS
    query = urlencode({"timestamp.gte": start, "timestamp.lt": start + DAY_NS,
                       "limit": 50000, "sort": "timestamp", "order": "asc"})
    with db:
        db.execute("INSERT OR IGNORE INTO partitions(symbol,kind,day,next_url) VALUES(?,?,?,?)",
                   (*key, API + path + "?" + query))
    while True:
        url, page, total = db.execute(
            "SELECT next_url,pages,records FROM partitions WHERE (symbol,kind,day)=(?,?,?)", key
        ).fetchone()
        if url is None:
            return total
        response = fetch(safe_url(url, path))
        if response.get("status") not in {"OK", "DELAYED"}:
            raise ValueError("Unexpected provider status; partition is incomplete")
        records = response.get("results", [])
        if not isinstance(records, list):
            raise ValueError("Invalid results list")
        for row in records:
            stamp = row["sip_timestamp"]
            if type(stamp) is not int or not start <= stamp < start + DAY_NS:
                raise ValueError("Unexpected SIP timestamp or UTC day boundary")
        next_url = response.get("next_url")
        if next_url is not None:
            next_url = safe_url(next_url, path)
            if next_url == url or db.execute(
                "SELECT 1 FROM pages WHERE (symbol,kind,day,source_url)=(?,?,?,?)", (*key, next_url)
            ).fetchone():
                raise ValueError("Repeated pagination cursor")
        raw = json.dumps(records, separators=(",", ":"), allow_nan=False).encode()
        payload = gzip.compress(raw, compresslevel=3, mtime=0)
        with db:
            changed = db.execute(
                """UPDATE partitions SET next_url=?, pages=pages+1, records=records+?
                   WHERE (symbol,kind,day,next_url)=(?,?,?,?)""",
                (next_url, len(records), *key, url)).rowcount
            if changed:
                db.execute("INSERT INTO pages VALUES(?,?,?,?,?,?,?,?,?)",
                           (*key, page + 1, url, response.get("request_id"),
                            datetime.now(timezone.utc).isoformat(), hashlib.sha256(raw).hexdigest(), payload))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--symbols", nargs="+", required=True)
    parser.add_argument("--feeds", nargs="+", choices=KINDS, default=list(KINDS))
    parser.add_argument("--start", type=date.fromisoformat, required=True)
    parser.add_argument("--end", type=date.fromisoformat, required=True, help="Exclusive UTC date")
    parser.add_argument("--db", type=Path, required=True)
    args = parser.parse_args()
    key = os.environ.get("MASSIVE_API_KEY")
    if not key:
        parser.error("Set MASSIVE_API_KEY in the process environment")
    if not args.start < args.end <= datetime.now(timezone.utc).date():
        parser.error("Choose a non-empty range of completed UTC days")
    db = database(args.db)
    try:
        day = args.start
        while day < args.end:
            for symbol in args.symbols:
                for kind in args.feeds:
                    count = download_day(db, symbol, kind, day, lambda url: request_json(url, key))
                    print(f"{day} {symbol} {kind}: {count} records", flush=True)
            day += timedelta(days=1)
    finally:
        db.close()


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, sqlite3.Error) as error:
        sys.exit(str(error))
