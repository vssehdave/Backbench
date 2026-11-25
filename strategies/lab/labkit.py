"""Run one lab strategy through customlib (xsection.run_window) and write the standard report.

Usage: python strategies/lab/labkit.py strategies/lab/NN-name/manifest.json insample|holdout|tune
  insample  2016-01-01..2023-12-31, results/insample/ (200 Monte Carlo paths)
  holdout   2024-01-01..latest bar, results/holdout/ (1000 paths), then the win-rule verdict against SPY
  tune      every manifest level on the in-sample window, no Monte Carlo (design only)
The manifest is an xs manifest plus "universe"; levels[0] is the frozen parameter set. See strategies/lab/LOG.md.
"""
import importlib
import json
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT)]
import customlib
import report
import xs_data
import xsection

FETCH = (date(2015, 1, 1), date(2026, 11, 25))  # one cached fetch; each phase slices it
PHASES = {"insample": (date(2015, 1, 1), date(2016, 1, 1), date(2024, 1, 1), 200),
          # The holdout panel starts late so the Monte Carlo bootstrap draws holdout-era days (plus the warm-up year).
          "holdout": (date(2022, 11, 1), date(2024, 1, 1), FETCH[1], 1000)}
# 5 bps a side, no commission; 5% a year on any borrowed cash so leverage is not free.
COSTS = xsection.Costs(commission_per_share=0., commission_min=0., slippage_bps=5., margin_bps=500.)
UNIVERSE = ("SPY", "QQQ", "IWM", "EFA", "EEM", "TLT", "IEF", "SHY", "GLD", "DBC", "VNQ", "LQD", "HYG",
            "XLB", "XLE", "XLF", "XLI", "XLK", "XLP", "XLU", "XLV", "XLY", "SSO", "QLD",
            # Round 2: commodity, FX, bond, 2x and factor ETFs (all with bars from 2016-01-04).
            "SLV", "USO", "DBA", "DBB", "CPER", "UUP", "FXE", "FXY", "FXA", "FXB", "FXF", "FXC", "TIP", "EMB",
            "UBT", "UGL", "EFO", "EET", "UGE", "RXL", "UPW", "SPLV", "USMV", "QUAL", "MTUM", "VLUE", "SIZE")


def panel(lo, hi):
    """xs_data.Panel of UNIVERSE on SPY's sessions in [lo, hi), from one cached fetch (as strategies/custom/faa)."""
    symbols = sorted(set(UNIVERSE))
    adj_rows, raw_rows = (xs_data.fetch_bars(symbols, *FETCH, k, data_dir=ROOT / "data/alpaca_xs") for k in ("all", "raw"))
    dates = [date.fromisoformat(d) for d, _ in adj_rows["SPY"] if lo <= date.fromisoformat(d) < hi]
    adj, raw = {}, {}
    for s in symbols:
        for rows, out in ((adj_rows[s], adj), (raw_rows[s], raw)):
            by = {date.fromisoformat(d): c for d, c in rows}
            out[s] = [by.get(d) for d in dates]
    return xs_data.Panel(dates, adj, raw, None, dict(symbols=symbols, sessions=len(dates)))


def load(manifest_path):
    m = json.loads(Path(manifest_path).read_text(encoding="utf-8"))
    sys.path.insert(0, str(Path(manifest_path).resolve().parent))
    module, fn = m["entry"].split(":")
    return m, getattr(importlib.import_module(module), fn)


def verdict(s, b, mc_s, mc_b):
    """The win rule on holdout metrics s (strategy) and b (SPY); mc_* are Monte Carlo p95 max drawdowns (positive)."""
    cagr_ok = s["cagr"] >= b["cagr"] or (abs(s["max_drawdown"]) < abs(b["max_drawdown"]) / 2 and s["cagr"] >= .8 * b["cagr"])
    checks = dict(sharpe=s["sharpe"] > b["sharpe"], sortino=s["sortino"] > b["sortino"], alpha=s["alpha"] > 0,
                  mc_p95=mc_s <= mc_b, cagr=cagr_ok)
    return all(checks.values()), checks


def main(argv=None):
    path, phase = (argv or sys.argv[1:])[:2]
    m, decide = load(path)
    limits = xsection.Limits(**m["limits"])
    if phase == "tune":
        lo, start, end, _ = PHASES["insample"]
        p = panel(lo, end)
        for level in m["levels"]:
            r = customlib.run_panel(p, lambda seen, _, lv=level: decide(seen, lv), limits, m["cadence"], start,
                                    costs=COSTS)
            k = r["metrics"]
            print(f"{json.dumps(level)} cagr={k['cagr']:.1%} sharpe={k['sharpe']:.2f} sortino={k['sortino']:.2f} "
                  f"dd={k['max_drawdown']:.1%} turn={r['turnover_per_year']:.1f}x cost={r['costs_pct_of_avg_equity_per_year']:.2%}")
        return
    lo, start, end, paths = PHASES[phase]
    p = panel(lo, end)
    level = m["levels"][0]
    customlib.report_panel(Path(path).parent, phase, p, lambda _: (lambda seen, __: decide(seen, level)), limits,
                           m["cadence"], start, COSTS, paths=paths)
    r = json.loads((Path(path).parent / "results" / phase / "report.json").read_text(encoding="utf-8"))
    s, b = r["metrics"]["strategy"], r["metrics"]["SPY"]
    mc_s = r["monte_carlo"]["strategy"]["max_drawdown"]["p95"]
    mc_b = r["monte_carlo"]["benchmark (SPY)"]["max_drawdown"]["p95"]
    for name, x, mc in (("strategy", s, mc_s), ("SPY", b, mc_b)):
        print(f"{phase} {name:8} cagr={x['cagr']:.1%} sharpe={x['sharpe']:.2f} sortino={x['sortino']:.2f} "
              f"alpha={x['alpha']:.1%} beta={x['beta']:.2f} dd={x['max_drawdown']:.1%} mc_p95={mc:.1%}")
    print(f"fills={r['fills']} decisions={r['result']['decisions']} costs={r['result']['costs_usd']}")
    if phase == "holdout":
        win, checks = verdict(s, b, mc_s, mc_b)
        print("WIN" if win and r["fills"] else "LOSS", checks)


if __name__ == "__main__":
    main()
