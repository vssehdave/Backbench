"""Run every xs strategy (catalog xs_manifest.json files and strategies/xs/*.json) with the standard report and Monte Carlo.

python strategies/xs/run_catalog.py [--paths 200]   (run from the repo root; needs the cached data/ or Alpaca keys)
One S&P 500 panel and one ETF panel per tradable set are shared. Each folder gets results/ (REPORT.md, report.json,
equity.svg, trade logs) and mc_results.json, as `python money.py mc <manifest>` writes them. Stock results are
survivorship-biased; report.json carries the strategy's LABELS.
"""
import argparse
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
import mc_runs  # noqa: E402
import xs_data  # noqa: E402
import xsection  # noqa: E402

CATALOG = ROOT / "strategies" / "catalog"
SECTORS = ["XLB", "XLC", "XLE", "XLF", "XLI", "XLK", "XLP", "XLRE", "XLU", "XLV", "XLY"]
FACTORS = ["SPY", "IWM", "IVE", "IVW", "MTUM"]
# Alpaca SIP bars begin 2016-01-04, so 2016 is the warm-up year for the 252-session lookbacks.
START, END, FETCH = date(2017, 1, 1), date(2026, 11, 1), date(2015, 1, 1)


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


def manifests():
    """[(manifest, tradable ETFs or None for the S&P 500 panel)]: every catalog xs_manifest.json, then strategies/xs."""
    out = []
    for manifest in sorted(CATALOG.glob("*/xs_manifest.json")):
        name = manifest.parent.name
        tradable = SECTORS + (["GLD"] if name.startswith("4.1.2") else []) if name.startswith("4.") else None
        out.append((manifest, tradable))
    return out + [(m, None) for m in sorted(Path(__file__).parent.glob("*.json")) if not m.stem.startswith("mc_results")]


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--paths", type=int, default=200)
    p.add_argument("--slow-paths", type=int, default=100, help="paths for the names given in --slow")
    p.add_argument("--slow", nargs="*", default=[], help="folder or file stems that get --slow-paths")
    p.add_argument("--only", nargs="*", default=None, help="run only these folder or file stems")
    args = p.parse_args(argv)
    todo = [(m, t) for m, t in manifests()
            if args.only is None or (m.parent.name if m.parent.parent == CATALOG else m.stem) in args.only]
    sp, etf_sets = None, {}
    for manifest, tradable in todo:
        key = manifest.parent.name if manifest.parent.parent == CATALOG else manifest.stem
        if tradable:
            if tuple(tradable) not in etf_sets:
                etf_sets[tuple(tradable)] = etf_panel(tradable)
            panel = etf_sets[tuple(tradable)]
        else:
            sp = sp or xs_data.build_panel(FETCH, END, log=print)
            panel = sp
        labels = xsection.load_manifest(manifest)[1][0].__globals__.get("LABELS", [])
        labels = sorted(set(labels + ([] if tradable else ["survivorship-biased"])))
        mc_runs.run_xs(manifest, START, END, args.slow_paths if key in args.slow else args.paths, 0, 20., panel,
                       dict(labels=labels))


if __name__ == "__main__":
    main()
