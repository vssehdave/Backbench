"""Momentum sleeve with a fast vol brake: hold the `top` assets with the best mean return over `lookbacks`, weighted
inverse-vol (`vol_days`), and cap the mix at `target` vol over the last `fast_days` sessions; the rest sits in SHY.
SHY until the longest lookback exists."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sig


def decide(seen, p):
    score = {}
    for s in p["assets"]:
        r = [sig.ret(seen, s, n) for n in p["lookbacks"]]
        if None in r:
            return {"SHY": 1.0}
        score[s] = sum(r) / len(r)
    picks = sorted(score, key=score.get, reverse=True)[:p["top"]]
    return sig.vol_cap(seen, sig.inverse_vol(seen, picks, p["vol_days"]), p["fast_days"], p["target"])
