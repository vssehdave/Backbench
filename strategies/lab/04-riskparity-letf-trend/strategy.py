"""Inverse-vol weights over `assets` (2x equity ETFs plus diversifiers), no margin. A leveraged sleeve whose underlying
(`trend` map) is below its `sma`-session moving average is moved to SHY.

Holds the assets equally until 60 sessions of history exist; the trend brake starts once `sma` sessions exist."""
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
    for s, under in p["trend"].items():
        if (sig.sma_ratio(seen, under, p["sma"]) or 1) < 1:
            w["SHY"] = w.get("SHY", 0) + w.pop(s)
    return w
