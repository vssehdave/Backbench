"""Signal helpers for lab strategies. seen is an xsection.AsOf: closes up to and including the decision day."""
import math
import statistics


def closes(seen, symbol, n):
    """The last n adjusted closes of symbol, or None with too little history."""
    p = [x for x in seen.prices.get(symbol, ()) if x is not None]
    return p[-n:] if len(p) >= n else None


def sma_ratio(seen, symbol, n):
    """close / n-session simple moving average, or None."""
    p = closes(seen, symbol, n)
    return p and p[-1] / statistics.fmean(p)


def ret(seen, symbol, n):
    """Return over the last n sessions, or None."""
    p = closes(seen, symbol, n + 1)
    return p and p[-1] / p[0] - 1


def vol(seen, symbol, n):
    """Annualized stdev of the last n daily returns, or None."""
    p = closes(seen, symbol, n + 1)
    return p and statistics.stdev([b / a - 1 for a, b in zip(p, p[1:])]) * math.sqrt(252)
