"""Point-in-time top-N S&P 500 universe by market cap, and per-trade features known before the entry. See docs/orb-top50.md.

Caps come from leader_rules.market_caps (EDGAR share counts priced on the filing day), called with the ranking day
replaced by the day before it, so a filing dated on the ranking day itself is not used.
"""
import bisect
import hashlib
import importlib.util
from datetime import date, timedelta
from pathlib import Path

import alpaca_bars
import edgar
import intraday

_RULES = Path(__file__).parent / "strategies/custom/sp500-top-holding/leader_rules.py"
_spec = importlib.util.spec_from_file_location("leader_rules", _RULES)  # that folder name has hyphens, so no plain import
leader_rules = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(leader_rules)

ATR_DAYS, BETA_DAYS, BETA_MIN = 20, 250, 60


def load_shares(symbols, data_dir=Path("data/edgar")):
    """{symbol: (cik, Shares)} for symbols with EDGAR facts. Delisted tickers have no CIK and are skipped."""
    ciks, out = edgar.ticker_map(data_dir), {}
    for s in symbols:
        record = edgar.company(ciks[s], data_dir) if s in ciks else None
        if record:
            out[s] = (ciks[s], leader_rules.Shares(record["dei_shares"], record["gaap_shares"]))
    return out


def ranking_index(dates, year, month):
    """Index of the last session strictly before the first of the month, or None."""
    n = bisect.bisect_left(dates, date(year, month, 1))
    return n - 1 if n else None


def top_by_cap(panel, shares, months, n=50):
    """{(year, month): [(symbol, cap), ...]} top n S&P members by cap, ranked on the prior month's last session.

    Uses members after that close, prices up to that close and filings dated strictly before it.
    """
    out = {}
    for year, month in months:
        i = ranking_index(panel.dates, year, month)
        if i is None:
            continue
        dates = panel.dates[:i] + [panel.dates[i] - timedelta(days=1)]  # filings on the ranking day itself stay hidden
        caps = leader_rules.market_caps(i, dates, panel.adj, panel.raw, shares, panel.members[i])
        out[(year, month)] = sorted(caps.items(), key=lambda kv: (-kv[1], kv[0]))[:n]
    return out


def daily_hl(symbols, start, end, data_dir=intraday.DATA, size=25):
    """{symbol: {date: (adj high, adj low, adj close)}} from SIP 1Day bars with adjustment=all (cached)."""
    symbols, out, headers = sorted(set(symbols)), {}, alpaca_bars.credentials()
    for n in range(0, len(symbols), size):
        group = symbols[n:n + size]
        key = hashlib.sha256("|".join(group).encode()).hexdigest()[:12]

        def build(group=group):
            params = {"symbols": ",".join(group), "timeframe": "1Day", "adjustment": "all", "feed": "sip",
                      "limit": 10000, "sort": "asc", "start": f"{start}T00:00:00Z", "end": f"{end}T00:00:00Z"}
            bars, pages = {}, alpaca_bars._pages("/v2/stocks/bars", params, headers)
            for page in pages:
                for symbol, rows in (page.get("bars") or {}).items():
                    bars.setdefault(symbol, []).extend([intraday._day(r["t"]).isoformat(), r["h"], r["l"], r["c"]] for r in rows)
            return bars, len(pages)
        for symbol, rows in intraday._cached(Path(data_dir) / f"dailyhl_{start}_{end}_{key}.json", build).items():
            out[symbol] = {date.fromisoformat(d): (h, l, c) for d, h, l, c in rows}
    return out


class History:
    """Daily features for one symbol, each computed from sessions strictly before the day asked about.

    daily is merge_daily rows (raw open, raw close, raw volume, adj open, adj close); hl is daily_hl rows; spy is the
    same merge_daily rows for SPY.
    """

    def __init__(self, daily, hl, spy):
        self.days = sorted(daily)
        self.daily, self.hl, self.spy = daily, hl, spy
        self._by_month = {}
        for d in self.days:
            self._by_month.setdefault((d.year, d.month), []).append(d)

    def _before(self, day, n):
        k = bisect.bisect_left(self.days, day)
        return self.days[max(k - n, 0):k]

    def atr_pct(self, day):
        """Mean true range over the 20 prior sessions as a fraction of the prior adjusted close."""
        window = self._before(day, ATR_DAYS + 1)
        if len(window) < ATR_DAYS + 1 or not all(d in self.hl for d in window):
            return None
        ranges = []
        for a, b in zip(window, window[1:]):
            high, low, _ = self.hl[b]
            ranges.append(max(high - low, abs(high - self.hl[a][2]), abs(low - self.hl[a][2])))
        return sum(ranges) / len(ranges) / self.hl[window[-1]][2]

    def gap(self, day):
        """Adjusted open on `day` over the prior adjusted close, minus 1. The open itself is known at 09:30."""
        prior = self._before(day, 1)
        return self.daily[day][3] / self.daily[prior[0]][4] - 1 if prior and day in self.daily else None

    def dollar_volume(self, day):
        """Mean raw close x raw volume per session over the calendar month before `day`'s month."""
        year, month = (day.year - 1, 12) if day.month == 1 else (day.year, day.month - 1)
        rows = [self.daily[d] for d in self._by_month.get((year, month), ())]
        return sum(r[1] * r[2] for r in rows) / len(rows) if rows else None

    def prior_close(self, day):
        prior = self._before(day, 1)
        return self.daily[prior[0]][1] if prior else None

    def beta(self, day):
        """Slope of daily adjusted returns on SPY over up to 250 sessions ending the session before `day`."""
        window = self._before(day, BETA_DAYS + 1)
        pairs = [(self.daily[b][4] / self.daily[a][4] - 1, self.spy[b][4] / self.spy[a][4] - 1)
                 for a, b in zip(window, window[1:]) if all(d in self.spy for d in (a, b))]
        if len(pairs) < BETA_MIN:
            return None
        mx, my = (sum(p[i] for p in pairs) / len(pairs) for i in (1, 0))
        var = sum((p[1] - mx) ** 2 for p in pairs)
        return sum((p[1] - mx) * (p[0] - my) for p in pairs) / var if var else None


def sectors(html_path=Path("data/sp500/constituents.html")):
    """{symbol: GICS sector} for today's S&P 500 members only; anything removed since is absent (reported as unknown)."""
    import xs_data
    parser = xs_data._Rows("constituents")
    parser.feed(Path(html_path).read_text(encoding="utf-8"))
    return {r[0].upper(): r[2] for r in parser.rows if len(r) > 2}
