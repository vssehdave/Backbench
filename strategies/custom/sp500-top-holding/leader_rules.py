"""Largest S&P 500 member by market cap, from EDGAR shares known on the date and Alpaca prices."""
from bisect import bisect_left, bisect_right


MAX_JUMP = 100  # a share count changing more than 100x versus the median of its own series is treated as a unit error


class Shares:
    """Share-count facts for one company (one CIK), usable only from the day they were filed.

    Facts are grouped by (filed, accession, period end); values within a group are summed, which adds up the
    share classes a company reports on one cover page (Alphabet, Fox, News Corp).
    """

    def __init__(self, dei, gaap=()):
        self.groups = self._group(dei) or self._group(gaap)
        self.filed = [g[0] for g in self.groups]

    @staticmethod
    def _group(rows):
        groups = {}
        for filed, end, accn, val in rows:
            groups.setdefault((filed, end, accn), set()).add(val)  # a repeated identical value is one class
        rows = sorted((f, e, sum(v)) for (f, e, _), v in groups.items())
        # Filers sometimes report a count 1000x too large (a unit slip): drop values far from the series median.
        mid = sorted(r[2] for r in rows)[len(rows) // 2] if rows else 1

        def sane(k):
            return mid / MAX_JUMP < rows[k][2] < mid * MAX_JUMP
        return [r for k, r in enumerate(rows) if sane(k)]

    def at(self, day):
        """(period_end, shares) from the most recently filed report with filed <= day, else None."""
        n = bisect_right(self.filed, str(day))
        return None if n == 0 else (self.groups[n - 1][1], self.groups[n - 1][2])


def market_caps(i, dates, adj, raw, shares, members):
    """{symbol: cap} on session i, one entry per CIK, using only filings dated on or before dates[i].

    cap = shares x raw close on the period end x adj[i] / adj[end]: the adjusted ratio carries the price forward
    in the share count's own terms, so a split between the period end and i does not distort the cap.
    shares maps symbol -> (cik, Shares). The first symbol alphabetically with data represents a CIK.
    """
    out, seen = {}, set()
    iso = [str(d) for d in dates]
    for s in sorted(members):
        if s not in shares or adj[s][i] is None:
            continue
        cik, record = shares[s]
        if cik in seen:
            continue
        fact = record.at(dates[i])
        if fact is None:
            continue
        e = max(bisect_right(iso, fact[0]) - 1, 0)
        if raw[s][e] is None or adj[s][e] is None:
            continue
        seen.add(cik)
        out[s] = fact[1] * raw[s][e] * adj[s][i] / adj[s][e]
    return out


def leader(i, dates, adj, raw, shares, members):
    caps = market_caps(i, dates, adj, raw, shares, members)
    return max(caps, key=caps.get) if caps else None


def make_decide(panel, shares, lag=1):
    """Strategy for xsection: 100% in the leader computed `lag` sessions before the decision close."""
    index = {d: i for i, d in enumerate(panel.dates)}

    def decide(seen, params):
        i = index[seen.date] - lag
        if i < 0:
            return None
        top = leader(i, panel.dates, panel.adj, panel.raw, shares, panel.members[i])
        return {top: 1.0} if top in seen.prices else None  # shortcut: if the lagged leader has no bar today, hold as is
    return decide
