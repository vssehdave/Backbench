"""Inverse-volatility weights over `assets`, scaled so the mix (ignoring correlation) hits `target` vol, gross <= cap.

Monthly. Before 60 sessions of history it holds the assets equally."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sig


def decide(seen, p):
    vols = {s: sig.vol(seen, s, p["vol_days"]) for s in p["assets"]}
    if None in vols.values():
        return {s: 1 / len(vols) for s in vols}
    inv = {s: 1 / v for s, v in vols.items()}
    w = {s: x / sum(inv.values()) for s, x in inv.items()}
    # Portfolio vol with the realised covariance of the same window.
    n = p["vol_days"]
    rets = {s: [b / a - 1 for a, b in zip(sig.closes(seen, s, n + 1), sig.closes(seen, s, n + 1)[1:])] for s in w}
    port = [sum(w[s] * rets[s][i] for s in w) for i in range(n)]
    pv = sig.statistics.stdev(port) * 252 ** .5
    k = min(p["cap"], p["target"] / pv)
    return {s: x * k for s, x in w.items()}
