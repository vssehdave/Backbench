"""Long-only multi-asset trend on ETF proxies for commodities, FX, bonds and non-US equity (no US equity, so it is a
second return stream next to 05). An asset is held when its mean return over `lookbacks` is positive; held assets get
their inverse-vol share of the whole universe (so fewer trends means more SHY), then the mix is capped at `target` vol
on a `fast_days` window. SHY until the longest lookback exists."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sig


def decide(seen, p):
    w = sig.inverse_vol(seen, p["assets"], p["vol_days"])
    if w is None:
        return {"SHY": 1.0}
    held = {}
    for s, x in w.items():
        r = [sig.ret(seen, s, n) for n in p["lookbacks"]]
        if None in r:
            return {"SHY": 1.0}
        if sum(r) > 0:
            held[s] = x
    out = sig.vol_cap(seen, held, p["fast_days"], p["target"]) if held else {"SHY": 1.0}
    out["SHY"] = out.get("SHY", 0) + 1 - sum(out.values())
    return out
