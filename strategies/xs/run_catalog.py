"""Run every catalog xs strategy on one cached S&P 500 panel and one ETF panel; write xs_results.json per folder.

python strategies/xs/run_catalog.py   (run from the repo root; needs the cached data/ or Alpaca keys)
Results are survivorship-biased and each carries the strategy's LABELS. Equity curves and decision logs are dropped to
keep the committed files small; rerun the script to regenerate them (or use `python money.py xs <manifest>`).
"""
import json
import statistics
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import xs_data  # noqa: E402
import xsection  # noqa: E402

CATALOG = ROOT / "strategies" / "catalog"
SECTORS = ["XLB", "XLC", "XLE", "XLF", "XLI", "XLK", "XLP", "XLRE", "XLU", "XLV", "XLY"]
FACTORS = ["SPY", "IWM", "IVE", "IVW", "MTUM"]
START, END, FETCH = date(2016, 1, 1), date(2026, 11, 1), date(2015, 1, 1)


def etf_panel(tradable, data_dir=ROOT / "data" / "alpaca_xs"):
    """Sector ETFs are tradable (members); factor ETFs, SPY and GLD sit in the panel but only as aux or benchmark."""
    names = sorted(set(SECTORS) | set(FACTORS) | {"GLD"})
    adj = xs_data.fetch_bars(names, FETCH, END, "all", data_dir=data_dir)
    raw = xs_data.fetch_bars(names, FETCH, END, "raw", data_dir=data_dir)
    dates = [date.fromisoformat(d) for d, _ in adj["SPY"]]
    index = {d: i for i, d in enumerate(dates)}

    def column(rows):
        out = [None] * len(dates)
        for d, c in rows:
            if date.fromisoformat(d) in index:
                out[index[date.fromisoformat(d)]] = c
        return out

    a = {s: column(adj[s]) for s in names}
    r = {s: column(raw[s]) for s in names}
    panel = xs_data.Panel(dates, a, r, [frozenset(tradable)] * len(dates))
    panel.aux = {s: a[s] for s in FACTORS}
    return panel


def summarize(report):
    traded = [f for f in report["folds"] if f["decisions"] > 0]
    out = dict(folds_total=len(report["folds"]), folds_traded=len(traded))
    if not traded:
        return out
    pick = {"strategy": lambda f: f["strategy"], "equal_weight": lambda f: f["benchmarks"]["equal_weight_universe"],
            "spy": lambda f: f["benchmarks"]["spy"], "cash": lambda f: f["benchmarks"]["cash"]}
    for name, get in pick.items():
        r = [get(f)["total_return"] for f in traded]
        s = [get(f)["sharpe"] for f in traded if get(f)["sharpe"] is not None]
        out[name] = dict(mean_return=statistics.fmean(r), median_return=statistics.median(r),
                         mean_sharpe=statistics.fmean(s) if s else None)
    out["mean_cost_drag"] = statistics.fmean(f["cost_drag"] for f in traded)
    out["mean_turnover_per_year"] = statistics.fmean(f["turnover_per_year"] for f in traded)
    return out


def main():
    sp = xs_data.build_panel(FETCH, END, log=print)
    etf_sets = {}
    rows = []
    for manifest in sorted(CATALOG.glob("*/xs_manifest.json")):
        folder = manifest.parent
        is_etf = folder.name.startswith("4.")
        if is_etf:
            tradable = SECTORS + (["GLD"] if folder.name.startswith("4.1.2") else [])
            key = tuple(tradable)
            etf_sets.setdefault(key, etf_panel(tradable))
            panel = etf_sets[key]
        else:
            panel = sp
        report = xsection.run(manifest, START, END, panel)
        labels = xsection.load_manifest(manifest)[1][0].__globals__["LABELS"] + ["survivorship-biased"]
        for f in report["folds"]:
            f.pop("equity"), f.pop("bench_equity"), f.pop("decision_log")
        report["labels"] = sorted(set(labels))
        report["summary"] = summarize(report)
        if is_etf:
            report["data"]["survivorship"] = None
        (folder / "xs_results.json").write_text(json.dumps(report, indent=1, default=str), encoding="utf-8")
        rows.append((folder.name, report["summary"]))
        print(folder.name, json.dumps(report["summary"], default=str)[:400], flush=True)
    return rows


if __name__ == "__main__":
    main()
