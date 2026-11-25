"""Inverse-vol weights (window `vol_days`) over `assets` (2x equity ETF plus diversifiers), no margin. The mix is scaled
so its realised vol over the last `fast_days` sessions hits `target`; the unused weight sits in SHY.

The fast window is the brake: it shrinks the 2x sleeve within a week or two of a volatility spike, without a price
trend rule. Holds the assets equally until `vol_days` sessions of history exist."""
import statistics
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
    n = p["fast_days"]
    rets = {}
    for s in w:
        c = sig.closes(seen, s, n + 1)
        rets[s] = [b / a - 1 for a, b in zip(c, c[1:])]
    pv = statistics.stdev([sum(w[s] * rets[s][i] for s in w) for i in range(n)]) * 252 ** .5
    k = min(1.0, p["target"] / pv)
    out = {s: x * k for s, x in w.items()}
    out["SHY"] = out.get("SHY", 0) + 1 - k
    return out
