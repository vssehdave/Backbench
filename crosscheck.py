"""Compare two daily row sets: python crosscheck.py CSV SYMBOL START END (CSV vs Alpaca)."""
import statistics
import sys
from datetime import date


def compare(a, b):
    ra, rb = {r[0]: r for r in a}, {r[0]: r for r in b}
    out = {"sessions": len(ra.keys() & rb.keys()), "only_a": sorted(ra.keys() - rb.keys()),
           "only_b": sorted(rb.keys() - ra.keys())}
    for name, i in (("open", 1), ("close", 2)):
        bps = [abs(ra[d][i] / rb[d][i] - 1) * 1e4 for d in ra.keys() & rb.keys()]
        out[name] = {"median_bps": statistics.median(bps), "max_bps": max(bps), "over_5_bps": sum(x > 5 for x in bps)}
    return out


if __name__ == "__main__":
    from alpaca_bars import daily_from_alpaca
    from minute_bars import daily_from_minutes
    path, symbol, start, end = sys.argv[1], sys.argv[2], date.fromisoformat(sys.argv[3]), date.fromisoformat(sys.argv[4])
    print(compare(daily_from_minutes(path, symbol, start, end)[0], daily_from_alpaca(symbol, start, end)[0]))
