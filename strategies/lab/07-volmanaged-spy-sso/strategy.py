"""Volatility-managed S&P exposure (Moreira-Muir style): exposure = min(cap, target / SPY's `vol_days` realised vol).
Exposure up to 1 is SPY plus SHY; above 1 it mixes SPY and SSO (2x), so no margin is used. SPY only until history exists."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sig


def decide(seen, p):
    v = sig.vol(seen, "SPY", p["vol_days"])
    if v is None:
        return {"SPY": 1.0}
    e = min(p["cap"], p["target"] / v)
    if e <= 1:
        return {"SPY": e, "SHY": 1 - e}
    return {"SSO": e - 1, "SPY": 2 - e}
