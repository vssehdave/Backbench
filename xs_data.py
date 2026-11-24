"""Cross-sectional data: S&P 500 membership by date and a many-stock Alpaca daily panel. See docs/cross-section.md."""
import hashlib
import json
import re
import urllib.request
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

import alpaca_bars

WIKI = "https://en.wikipedia.org/wiki/"
PAGES = {"constituents": ("List_of_S%26P_500_companies", "constituents"),
         "changes": ("Historical_components_of_the_S%26P_500", "changes")}
AGENT = "wallet-research/0.1 (personal research)"
BENCHMARK = "SPY"


class _Rows(HTMLParser):
    """Rows of td texts for the table with one id. Header rows (any th) are skipped."""

    def __init__(self, table_id):
        super().__init__()
        self.id, self.inside, self.row, self.cell, self.th, self.rows = table_id, 0, None, None, False, []

    def handle_starttag(self, tag, attrs):
        if tag == "table" and (self.inside or dict(attrs).get("id") == self.id):
            self.inside += 1
        elif self.inside and tag == "tr":
            self.row, self.th = [], False
        elif self.inside and tag in ("td", "th") and self.row is not None:
            self.cell, self.th = [], self.th or tag == "th"

    def handle_data(self, data):
        if self.cell is not None:
            self.cell.append(data)

    def handle_endtag(self, tag):
        if tag == "table" and self.inside:
            self.inside -= 1
        elif tag in ("td", "th") and self.cell is not None:
            self.row.append(re.sub(r"\[\w+\]|\s+", " ", "".join(self.cell)).strip())
            self.cell = None
        elif tag == "tr" and self.row is not None:
            if self.row and not self.th:
                self.rows.append(self.row)
            self.row = None


def _page(name, data_dir):
    """Cached HTML plus provenance (revision id, sha256, fetch time) for one Wikipedia page."""
    title, _ = PAGES[name]
    html_path, meta_path = Path(data_dir) / f"{name}.html", Path(data_dir) / f"{name}.json"
    if not (html_path.is_file() and meta_path.is_file()):
        request = urllib.request.Request(WIKI + title, headers={"User-Agent": AGENT})
        with urllib.request.urlopen(request, timeout=60) as reply:
            body = reply.read()
        revision = re.search(rb'"wgRevisionId":(\d+)', body)
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        html_path.write_bytes(body)
        meta_path.write_text(json.dumps(dict(url=WIKI + title, revision_id=revision and int(revision[1]),
                                             sha256=hashlib.sha256(body).hexdigest(),
                                             fetched_at_utc=datetime.now(timezone.utc).isoformat())), encoding="utf-8")
    meta = json.loads(meta_path.read_text(encoding="utf-8"))
    body = html_path.read_bytes()
    if hashlib.sha256(body).hexdigest() != meta["sha256"]:
        raise ValueError(f"Cached {name} page does not match its recorded sha256")
    return body.decode("utf-8"), meta


def fetch_universe(data_dir=Path("data/sp500")):
    """(current tickers, changes newest first, provenance). A change is (effective date, added, removed, reason)."""
    html, current_meta = _page("constituents", data_dir)
    parser = _Rows("constituents")
    parser.feed(html)
    current = sorted({r[0].upper() for r in parser.rows if r and r[0]})
    html, changes_meta = _page("changes", data_dir)
    parser = _Rows("changes")
    parser.feed(html)
    changes, malformed = [], 0
    for r in parser.rows:
        try:
            day = datetime.strptime(r[0], "%B %d, %Y").date()
        except ValueError:
            malformed += 1
            continue
        if len(r) < 6:
            malformed += 1
            continue
        changes.append((day, r[1].upper(), r[3].upper(), r[5]))
    changes.sort(key=lambda c: c[0], reverse=True)
    if len(current) < 400 or len(changes) < 100:
        raise ValueError(f"Parsed only {len(current)} members and {len(changes)} changes; the page layout changed")
    return current, changes, dict(constituents=current_meta, changes=changes_meta, malformed_change_rows=malformed)


def membership(current, changes, dates):
    """Member set after each date's close: start from today's list and undo every change effective after it.

    Returns (list of frozensets aligned to dates, count of changes that contradict the running set).
    """
    members, pending, bad = set(current), iter(changes), 0
    change = next(pending, None)
    out = [None] * len(dates)
    for i in range(len(dates) - 1, -1, -1):
        while change and change[0] > dates[i]:
            _, added, removed, _ = change
            if added:
                bad += added not in members
                members.discard(added)
            if removed:
                bad += removed in members
                members.add(removed)
            change = next(pending, None)
        out[i] = frozenset(members)
    return out, bad


def _digest(payload):
    return hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def _chunk(group, start, end, adjustment, feed, data_dir):
    key = hashlib.sha256("|".join(group).encode()).hexdigest()[:12]
    cache = Path(data_dir) / f"{adjustment}_{start}_{end}_{feed}_{key}.json"
    if cache.is_file():
        record = json.loads(cache.read_text(encoding="utf-8"))
        if _digest(record["bars"]) != record["provenance"]["bars_sha256"]:
            raise ValueError(f"Cached {cache.name} does not match its recorded sha256")
        return record["bars"]
    params = {"symbols": ",".join(group), "timeframe": "1Day", "adjustment": adjustment, "feed": feed,
              "limit": 10000, "sort": "asc", "start": f"{start}T00:00:00Z", "end": f"{end}T00:00:00Z"}
    bars = {}
    for page in alpaca_bars._pages("/v2/stocks/bars", params, alpaca_bars.credentials()):
        for symbol, rows in (page.get("bars") or {}).items():
            # A symbol's bars can span several pages, so extend rather than assign.
            bars.setdefault(symbol, []).extend(
                [datetime.fromisoformat(r["t"].replace("Z", "+00:00")).astimezone(alpaca_bars.EASTERN).date().isoformat(),
                 float(r["c"])] for r in rows)
    provenance = dict(source="alpaca", feed=feed, adjustment=adjustment, request=params, requested=group,
                      returned=sorted(bars), bars_sha256=_digest(bars), fetched_at_utc=datetime.now(timezone.utc).isoformat(),
                      note="Compact [date, close] rows; the raw JSON pages are not stored")
    cache.parent.mkdir(parents=True, exist_ok=True)
    temporary = cache.with_suffix(".tmp")
    temporary.write_text(json.dumps(dict(provenance=provenance, bars=bars)), encoding="utf-8")
    temporary.replace(cache)
    return bars


def fetch_bars(symbols, start, end, adjustment, feed="sip", data_dir=Path("data/alpaca_xs"), size=100, log=None):
    symbols, out = sorted(set(symbols)), {}
    for n in range(0, len(symbols), size):
        out.update(_chunk(symbols[n:n + size], start, end, adjustment, feed, data_dir))
        if log:
            log(f"{adjustment}: {min(n + size, len(symbols))}/{len(symbols)} symbols")
    return out


class Panel:
    """Aligned daily closes. adj (split and dividend adjusted) drives signals and returns; raw gives share counts.

    adj[s][i] and raw[s][i] are None where symbol s has no bar on dates[i]. members[i] is the S&P 500 set after
    that session's close, or None when the panel has no membership (synthetic tests).
    """

    def __init__(self, dates, adj, raw, members=None, quality=None):
        self.dates, self.adj, self.raw, self.members, self.quality = list(dates), adj, raw, members, quality or {}
        self.first = {s: next(i for i, p in enumerate(v) if p is not None) for s, v in adj.items()}
        self.last = {s: max(i for i, p in enumerate(v) if p is not None) for s, v in adj.items()}


def build_panel(start, end, data_dir=Path("data/alpaca_xs"), universe_dir=Path("data/sp500"), feed="sip", log=None,
                member_from=date(2016, 1, 1)):
    """Panel over [start, end) for every ticker that was an S&P 500 member on any session since member_from."""
    current, changes, universe_meta = fetch_universe(universe_dir)
    # A calendar-only first pass: membership needs session dates, and SPY supplies them.
    spy = fetch_bars([BENCHMARK], start, end, "all", feed, data_dir, log=log)[BENCHMARK]
    dates = [date.fromisoformat(d) for d, _ in spy]
    sets, inconsistent = membership(current, changes, dates)
    wanted = set().union(*(s for d, s in zip(dates, sets) if d >= member_from)) | {BENCHMARK}
    adj_rows = fetch_bars(wanted, start, end, "all", feed, data_dir, log=log)
    raw_rows = fetch_bars(wanted, start, end, "raw", feed, data_dir, log=log)
    index = {d: i for i, d in enumerate(dates)}
    adj, raw, off_calendar, mismatched, jumps = {}, {}, 0, [], []
    for symbol in sorted(set(adj_rows) & set(raw_rows)):
        a = {date.fromisoformat(d): c for d, c in adj_rows[symbol]}
        r = {date.fromisoformat(d): c for d, c in raw_rows[symbol]}
        if a.keys() != r.keys():
            mismatched.append(symbol)
            continue
        off_calendar += sum(d not in index for d in a)
        if not any(d in index for d in a):
            continue
        adj[symbol] = [a.get(d) for d in dates]
        raw[symbol] = [r.get(d) for d in dates]
        previous = None
        for i, price in enumerate(adj[symbol]):
            if price is not None and previous is not None and abs(price / previous - 1) > 0.5:
                jumps.append((symbol, str(dates[i]), round(price / previous - 1, 3)))
            previous = price if price is not None else previous
    quality = dict(symbols_requested=len(wanted), symbols_with_bars=len(adj), bars_off_spy_calendar=off_calendar,
                   adj_raw_date_mismatch=mismatched, adjusted_moves_over_50pct=jumps,
                   membership_inconsistencies=inconsistent, sessions=len(dates), universe=universe_meta)
    return Panel(dates, adj, raw, sets, quality)


def coverage(panel, first_index, last_index, tolerance=5):
    """How much of the historical S&P 500 membership has Alpaca data. Anything short of full is survivorship bias."""
    span = range(first_index, last_index + 1)
    ever, days, covered = {}, 0, 0
    for i in span:
        for s in panel.members[i]:
            ever.setdefault(s, []).append(i)
        days += len(panel.members[i])
        covered += sum(panel.adj.get(s, [None] * len(panel.dates))[i] is not None for s in panel.members[i])
    missing = sorted(s for s in ever if s not in panel.adj)
    late = sorted(s for s in ever if s in panel.adj and panel.first[s] > ever[s][0] + tolerance)
    early = sorted(s for s in ever if s in panel.adj and panel.last[s] < ever[s][-1] - tolerance)
    return dict(first=str(panel.dates[first_index]), last=str(panel.dates[last_index]), ever_members=len(ever),
                members_without_any_data=len(missing), missing_symbols=missing,
                data_starts_after_membership=len(late), data_ends_before_membership_ends=len(early),
                member_days=days, member_days_with_data=covered, member_day_coverage=covered / days,
                survivorship_biased=bool(missing or late or early or covered < days),
                late_symbols=late, early_symbols=early)
