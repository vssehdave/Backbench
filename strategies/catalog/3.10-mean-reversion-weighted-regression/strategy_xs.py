"""3.10 mean reversion, weighted regression: residuals of R on sector dummies with weights z_i = 1/sigma_i^2,
twiddled returns R~ = Z * eps (eq. 314), D_i = -gamma * R~_i, sum of |D_i| = 1.

PROXY: Omega is the sector dummy matrix only (the paper allows non-binary risk factors but fixes none) and the
sectors are the current GICS sectors from the cached Wikipedia page (lookahead; ex-members unclassified and dropped).
sigma_i is the daily-return volatility over `window` sessions; the return is the last 21 sessions.
"""
import math
import statistics
from pathlib import Path

LABELS = ["survivorship-biased S&P 500 universe",
          "proxy: current GICS sectors as the only regressors (lookahead, ex-members dropped)"]
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
    lookback, window, sector = params["lookback"], params["window"], params.get("sectors") or sectors()
    groups = {}
    for s, p in panel.prices.items():
        tail = p[-window - 1:]
        if s in sector and len(p) > max(lookback, window) and p[-1 - lookback] is not None \
                and len(tail) == window + 1 and None not in tail:
            var = statistics.variance(b / a - 1 for a, b in zip(tail, tail[1:]))
            if var > 0:
                groups.setdefault(sector[s], {})[s] = (math.log(p[-1] / p[-1 - lookback]), 1 / var)
    d = {}
    for members in groups.values():
        mean = sum(r * z for r, z in members.values()) / sum(z for _, z in members.values())
        d.update({s: -z * (r - mean) for s, (r, z) in members.items()})  # -Z * eps
    gross = sum(abs(x) for x in d.values())
    return {s: x / gross for s, x in d.items()} if gross else None
