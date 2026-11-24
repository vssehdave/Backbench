"""SEC EDGAR XBRL companyfacts, keyless: compact per-company extracts cached with the raw response sha256.

Every fact keeps its filing date, because a figure is only usable on or after the day it was filed.
"""
import hashlib
import json
import time
import urllib.error
import urllib.request
from datetime import date
from pathlib import Path

AGENT = "research-harness contact@example.com"  # generic on purpose
FACTS = "https://data.sec.gov/api/xbrl/companyfacts/CIK{:010d}.json"
TICKERS = "https://www.sec.gov/files/company_tickers.json"
PAUSE = 0.12  # seconds between requests: under the 10 per second limit
USD = {"NetIncomeLoss": "ni", "ProfitLoss": "ni2"}
INSTANT = {"StockholdersEquity": "eq", "StockholdersEquityIncludingPortionAttributableToNoncontrollingInterest": "eq2",
           "LongTermDebt": "ltd", "LongTermDebtNoncurrent": "ltd_nc", "LongTermDebtCurrent": "ltd_c",
           "DebtCurrent": "debt_c", "LongTermDebtAndCapitalLeaseObligations": "ltd_cap"}
_last = [0.]


def _get(url, retries=4):
    for attempt in range(retries + 1):
        wait = PAUSE - (time.monotonic() - _last[0])
        if wait > 0:
            time.sleep(wait)
        _last[0] = time.monotonic()
        try:
            request = urllib.request.Request(url, headers={"User-Agent": AGENT, "Accept-Encoding": "identity"})
            with urllib.request.urlopen(request, timeout=90) as reply:
                return reply.read()
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                return None
            if exc.code not in (429, 500, 502, 503) or attempt == retries:
                raise RuntimeError(f"SEC request failed (HTTP {exc.code})") from None
            time.sleep(2 ** attempt)


def ticker_map(data_dir=Path("data/edgar")):
    """Current ticker (Alpaca style, BRK.B) -> CIK. Delisted tickers are absent: a stated survivorship limit."""
    cache = Path(data_dir) / "company_tickers.json"
    if not cache.is_file():
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        cache.write_bytes(_get(TICKERS))
    return {v["ticker"].upper().replace("-", "."): int(v["cik_str"]) for v in json.loads(cache.read_text("utf-8")).values()}


def extract(raw):
    """Compact view of a companyfacts payload."""
    facts, out = raw.get("facts", {}), {}
    dei = facts.get("dei", {}).get("EntityCommonStockSharesOutstanding", {}).get("units", {}).get("shares", [])
    out["dei_shares"] = [[f["filed"], f["end"], f["accn"], f["val"]] for f in dei]
    gaap = facts.get("us-gaap", {})
    out["gaap_shares"] = [[f["filed"], f["end"], f["accn"], f["val"]]
                          for f in gaap.get("CommonStockSharesOutstanding", {}).get("units", {}).get("shares", [])]
    for tag, key in USD.items():  # annual durations only
        rows = gaap.get(tag, {}).get("units", {}).get("USD", [])
        out[key] = [[f["filed"], f["start"], f["end"], f["val"]] for f in rows if f.get("start") and f["form"] in ("10-K", "10-K/A", "10-KT")
                    and 340 <= (date.fromisoformat(f["end"]) - date.fromisoformat(f["start"])).days <= 380]
    for tag, key in INSTANT.items():
        out[key] = [[f["filed"], f["end"], f["val"]] for f in gaap.get(tag, {}).get("units", {}).get("USD", [])
                    if f["form"] in ("10-K", "10-K/A", "10-KT")]
    return out


def company(cik, data_dir=Path("data/edgar")):
    """Compact record for one CIK, or None if the SEC has no facts for it. Cached."""
    cache = Path(data_dir) / f"CIK{cik:010d}.json"
    if cache.is_file():
        return json.loads(cache.read_text("utf-8"))
    body = _get(FACTS.format(cik))
    record = None if body is None else dict(cik=cik, raw_sha256=hashlib.sha256(body).hexdigest(),
                                            raw_bytes=len(body), **extract(json.loads(body)))
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(record), encoding="utf-8")
    return record


def visible(rows, as_of):
    """Rows filed on or before as_of (ISO string or date); filed is column 0 and ISO strings sort by date."""
    as_of = str(as_of)
    return [r for r in rows if r[0] <= as_of]
