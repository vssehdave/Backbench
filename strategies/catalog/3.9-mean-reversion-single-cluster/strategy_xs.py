"""3.9 mean reversion, one cluster: dollar positions D_i = -gamma * demeaned log return, sum of |D_i| = 1.

The paper wants N highly correlated stocks (one industry); here the cluster is the whole S&P 500 universe, a
choice, so this is the unclustered version. Formation window t1..t2 is the last month (21 sessions); the paper gives none.
"""
import math

LABELS = ["survivorship-biased S&P 500 universe", "whole universe treated as one cluster; 1-month formation window"]


def decide(panel, params):
    lookback = params["lookback"]
    r = {s: math.log(p[-1] / p[-1 - lookback]) for s, p in panel.prices.items()
         if len(p) > lookback and p[-1 - lookback] is not None}
    if len(r) < 2:
        return None
    mean = sum(r.values()) / len(r)
    d = {s: mean - x for s, x in r.items()}  # -R~, eq. 297
    gross = sum(abs(x) for x in d.values())
    return {s: x / gross for s, x in d.items()} if gross else None
