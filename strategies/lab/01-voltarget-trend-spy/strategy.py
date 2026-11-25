"""SPY sized to a volatility target (levered up to `cap`), only while SPY is above its moving average; else SHY.

Holds SPY 100% until the signals have history (Alpaca bars start 2016-01-04)."""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import sig


def decide(seen, p):
    trend, v = sig.sma_ratio(seen, "SPY", p["sma"]), sig.vol(seen, "SPY", p["vol_days"])
    if trend is None or v is None:
        return {"SPY": 1.}
    if trend < 1:
        return {"SHY": 1.}
    w = min(p["cap"], p["target"] / v)
    return {"SPY": w, "SHY": 1 - w} if w < 1 else {"SPY": w}
