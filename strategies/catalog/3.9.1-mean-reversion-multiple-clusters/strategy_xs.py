"""3.9.1 mean reversion, K clusters: D_i = -gamma * (return demeaned within the stock's cluster), sum of |D_i| = 1.

PROXY: clusters are the current GICS sectors from the cached Wikipedia constituents page. That classification is
as of today (lookahead) and missing for names that left the index, so those names are left out.
"""
import math
from pathlib import Path

LABELS = ["survivorship-biased S&P 500 universe",
          "proxy: current GICS sectors as clusters (lookahead, ex-members unclassified and dropped)"]
_SECTORS = {}


def sectors():
    if not _SECTORS:
        import xs_data
        html, _ = xs_data._page("constituents", Path(__file__).resolve().parents[3] / "data" / "sp500")
        rows = xs_data._Rows("constituents")
        rows.feed(html)
        _SECTORS.update({r[0].upper(): r[2] for r in rows.rows if len(r) > 2})
    return _SECTORS


def decide(panel, params):
    lookback, sector = params["lookback"], params.get("sectors") or sectors()
    groups = {}
    for s, p in panel.prices.items():
        if s in sector and len(p) > lookback and p[-1 - lookback] is not None:
            groups.setdefault(sector[s], {})[s] = math.log(p[-1] / p[-1 - lookback])
    d = {}
    for members in groups.values():
        mean = sum(members.values()) / len(members)
        d.update({s: mean - x for s, x in members.items()})
    gross = sum(abs(x) for x in d.values())
    return {s: x / gross for s, x in d.items()} if gross else None
