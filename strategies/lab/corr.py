"""Daily-return correlation of lab strategies over the holdout: python strategies/lab/corr.py 05-x 08-y ...

Reruns each frozen manifest (first level) through customlib.run_panel without Monte Carlo; the win rule counts a new
winner as separate only if its correlation with every earlier winner is at most 0.8."""
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import labkit  # first: it puts the repo root on sys.path
import customlib
import xsection


def returns(folder, p, start):
    sys.modules.pop("strategy", None)  # every lab folder names its module strategy.py
    m, decide = labkit.load(Path(__file__).parent / folder / "manifest.json")
    level = m["levels"][0]
    r = customlib.run_panel(p, lambda seen, _: decide(seen, level), xsection.Limits(**m["limits"]), m["cadence"], start,
                            costs=labkit.COSTS)
    e = r["equity"]
    return [b / a - 1 for a, b in zip(e, e[1:])]


def main(folders):
    lo, start, end, _ = labkit.PHASES["holdout"]
    p = labkit.panel(lo, end)
    rets = {f: returns(f, p, start) for f in folders}
    for i, a in enumerate(folders):
        for b in folders[i + 1:]:
            print(f"{a} vs {b}: {statistics.correlation(rets[a], rets[b]):.2f}")


if __name__ == "__main__":
    main(sys.argv[1:])
