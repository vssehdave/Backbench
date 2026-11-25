"""Dual momentum over `assets`: hold the `top` assets with the best mean return over `lookbacks` sessions, equal weight.
A pick whose own score is below 0 (absolute momentum) is replaced by SHY. Holds SHY until the longest lookback exists."""
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
    w = {}
    for s in sorted(score, key=score.get, reverse=True)[:p["top"]]:
        k = s if score[s] > 0 else "SHY"
        w[k] = w.get(k, 0) + 1 / p["top"]
    return w
