"""Standard report for every catalog strategy, then strategies/catalog/INDEX.md. Run: python catalog_report.py --help.

The strategy list comes from the folders: each manifest beside a README.md is one run (engine from the file name), and a
folder with none is skipped with the reason its README gives. Cross-section runs go through strategies/xs/run_catalog.py.
"""
import argparse
import json
import re
import subprocess
import sys
import time
from datetime import date
from pathlib import Path

import mc_runs

ROOT = Path(__file__).parent
CATALOG = ROOT / "strategies" / "catalog"
PATTERNS = (("options", "options_manifest*.json"), ("xsection", "xs_manifest.json"), ("multi", "multi*.json"),
            ("harness", "manifest*.json"))
# Alpaca SIP daily bars begin 2016-01-04 and the harness warms up on the 12 months before start.
RUINED = "RUINED.txt"
START, END, OPTIONS_TODAY = date(2017, 1, 1), date(2026, 1, 1), date(2026, 11, 23)
SPY_COVID_DD = 0.338  # SPY close-to-close drawdown Feb-Mar 2020; any window holding 2020 must reproduce it
FLAG_PP = 0.05  # flag a CAGR that moved more than 5 percentage points from the old headline


def discover(catalog=CATALOG):
    """([(folder, manifest, engine)], [folders without a manifest]); a folder's first run is its primary."""
    runs, skipped = [], []
    for folder in sorted((p for p in catalog.iterdir() if (p / "README.md").exists()), key=lambda p: section_key(p.name)):
        found = [(folder, m, engine) for engine, pattern in PATTERNS for m in sorted(folder.glob(pattern))
                 if not m.name.endswith(".results.json")]
        runs += found
        if not found:
            skipped.append(folder)
    return runs, skipped


def section_key(name):
    return tuple(int(x) for x in re.match(r"[\d.]+", name).group().strip(".").split("."))


def readme(folder):
    """(section, strategy name, harness status) from the README header lines."""
    text = (folder / "README.md").read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ").strip()
    section = title.split(" ", 1)[0]
    status = re.search(r"Harness status: \*\*(.+?)\*\*", text)
    return section, title[len(section):].strip(), status.group(1) if status else "no manifest"


def report_path(manifest, engine):
    return mc_runs.out_dir(manifest, engine)[0] / "report.json"


def check(report, engine):
    """Fail loudly on a run that traded nothing or a SPY row that does not reproduce the 2020 drawdown."""
    if not report.get("fills"):
        raise RuntimeError(f"{report['name']}: no fills")
    config = report["mc_config"]
    spy = report["metrics"].get("SPY")
    if spy and config["start"] < "2020-02-01" and config["end"] > "2020-04-01":
        if abs(abs(spy["max_drawdown"]) - SPY_COVID_DD) > 0.01:
            raise RuntimeError(f"{report['name']}: SPY max drawdown {spy['max_drawdown']:.1%}, expected ~{SPY_COVID_DD:.1%}")


def old_cagr(headline, years):
    """Annualise an old INDEX headline: an explicit CAGR, a mean 6-month return, or a total return over `years`."""
    if m := re.search(r"CAGR ([-+]?\d+\.?\d*)%", headline):
        return float(m.group(1)) / 100
    if m := re.search(r"mean 6-month ([-+]?\d+\.?\d*)%", headline):
        return (1 + float(m.group(1)) / 100) ** 2 - 1
    if m := re.match(r"\s*([-+]?\d+\.?\d*)% vs B&H", headline):
        return (1 + float(m.group(1)) / 100) ** (1 / years) - 1
    return None


def old_headlines(index_text):
    """{folder: headline} from the old INDEX's last column."""
    out = {}
    for line in index_text.splitlines():
        if m := re.match(r"\|[^|]*\| \[[^]]*\]\(([^)]+)/\) \|.*\| tested[^|]*\|([^|]*)\|\s*$", line):
            out[m.group(1)] = m.group(2).strip()
    return out


def flags(runs, headlines):
    """[(folder, old CAGR, new CAGR)] for primaries whose CAGR moved more than FLAG_PP from the old headline."""
    out, seen = [], set()
    for folder, manifest, engine in runs:
        if folder.name in seen or folder.name not in headlines or not report_path(manifest, engine).exists():
            continue
        seen.add(folder.name)
        r = json.loads(report_path(manifest, engine).read_text(encoding="utf-8"))
        # Old harness and multi headlines compounded ten July-December windows: five years of exposure.
        years = 5. if engine in ("harness", "multi") else (date.fromisoformat(r["mc_config"]["end"])
                                                           - date.fromisoformat(r["mc_config"]["start"])).days / 365.25
        old, new = old_cagr(headlines[folder.name], years), r["metrics"]["strategy"]["cagr"]
        if old is not None and abs(new - old) > FLAG_PP:
            out.append((folder.name, old, new))
    return out


def pct(x):
    return "" if x is None else f"{x:.1%}"


def num(x):
    return "" if x is None else f"{x:.2f}"


def row(section, name, status, report, link, series="strategy", mc="strategy"):
    m, dd = report["metrics"][series], report["monte_carlo"][mc]["max_drawdown"]
    return (f"| {section} | {name} | {status} | {pct(m['cagr'])} | {num(m['sharpe'])} | {num(m['sortino'])} | "
            f"{num(m.get('beta'))} | {pct(m.get('alpha'))} | {pct(abs(m['max_drawdown']))} | {pct(dd['p95'])} | "
            f"[report]({link}) |")


def write_index(runs, skipped, catalog=CATALOG):
    head = ["| Section | Strategy | Status | CAGR | Sharpe | Sortino | beta | alpha | maxDD | MC DD p95 | Report |",
            "|---|---|---|---|---|---|---|---|---|---|---|"]
    body, missing = [], []
    bench = report_path(mc_runs.BENCHMARK, "harness")
    if bench.exists():
        r = json.loads(bench.read_text(encoding="utf-8"))
        # The harness buy-and-hold control keeps part cash; the row is plain SPY closes and their bootstrap.
        body.append(row("-", "SPY buy and hold", "benchmark", r, bench.parent.relative_to(catalog).as_posix() + "/REPORT.md",
                        "SPY", "benchmark full history (mode B)"))
    for folder, manifest, engine in runs:
        section, name, _ = readme(folder)
        path = report_path(manifest, engine)
        variant = path.parent.name if path.parent.name != "results" else ""
        label = f"[{name}]({folder.name}/)" + (f" ({variant})" if variant else "")
        if (path.parent / RUINED).exists():
            note = (path.parent / RUINED).read_text(encoding="utf-8").strip()
            body.append(f"| {section} | {label} | ruined ({engine}): {note} |  |  |  |  |  |  |  |  |")
            continue
        if not path.exists():
            missing.append(folder.name)
            body.append(f"| {section} | {label} | not run ({engine}) |  |  |  |  |  |  |  |  |")
            continue
        r = json.loads(path.read_text(encoding="utf-8"))
        body.append(row(section, label, f"tested ({engine})", r, path.parent.relative_to(catalog).as_posix() + "/REPORT.md"))
    for folder in skipped:
        section, name, status = readme(folder)
        body.append(f"| {section} | [{name}]({folder.name}/) | {status} |  |  |  |  |  |  |  |  |")
    tested = len({f for f, _, _ in runs})
    text = "\n".join([
        "# Strategy catalog", "",
        "Source: Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865. One folder per strategy "
        "section. Regenerate with `python catalog_report.py`.", "",
        f"Folders: {tested + len(skipped)}. Tested: {tested} ({len(runs)} runs). Not testable: {len(skipped)}.", "",
        f"Periods: harness and multi-asset {START} to {END}; cross-section {date(2017, 1, 1)} to {date(2026, 11, 1)} "
        f"(survivorship-biased S&P 500 panel); options 2024-01-19 to the last expiry before {OPTIONS_TODAY}. Metrics "
        "use daily equity, rf = 0; beta and alpha are against SPY; maxDD is the backtest's, MC DD p95 the 95th "
        "percentile of the Monte Carlo drawdown distribution. Each REPORT.md has p5/p50/p95/p99 and the trade days.", "",
        *head, *body, ""])
    (catalog / "INDEX.md").write_text(text, encoding="utf-8")
    return missing


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--paths", type=int, default=1000, help="paths for harness, multi and options runs")
    p.add_argument("--xs-paths", type=int, default=200)
    p.add_argument("--xs-slow-paths", type=int, default=100)
    p.add_argument("--xs-slow", nargs="*", default=[], help="xs folder or file stems that get --xs-slow-paths")
    p.add_argument("--engines", nargs="*", default=["benchmark", "harness", "multi", "options", "xsection"])
    p.add_argument("--only", nargs="*", default=None, help="folder names to run")
    p.add_argument("--index-only", action="store_true", help="skip runs; rebuild INDEX.md from existing reports")
    p.add_argument("--old-index", type=Path, default=CATALOG / "INDEX.md", help="INDEX with the old headlines")
    args = p.parse_args(argv)
    runs, skipped = discover()
    headlines = old_headlines(args.old_index.read_text(encoding="utf-8"))
    for folder in skipped:
        print(f"skip {folder.name}: {readme(folder)[2]}")
    todo = [r for r in runs if args.only is None or r[0].name in args.only]
    started = time.perf_counter()
    if not args.index_only:
        if "benchmark" in args.engines:
            mc_runs.run_single(mc_runs.BENCHMARK, START, END, args.paths, 0, 20., 20)
        for folder, manifest, engine in todo:
            if engine not in args.engines or engine == "xsection":
                continue
            if engine == "harness":
                mc_runs.run_single(manifest, START, END, args.paths, 0, 20., 20)
            elif engine == "multi":
                m = json.loads(manifest.read_text(encoding="utf-8"))  # Kraken serves only 720 days: BTC sets its own
                folder_out = mc_runs.out_dir(manifest, engine)[0]
                try:
                    mc_runs.run_multi(manifest, date.fromisoformat(m.get("start", str(START))),
                                      date.fromisoformat(m.get("end", str(END))), args.paths, 0, 20.)
                    (folder_out / RUINED).unlink(missing_ok=True)
                except mc_runs.Ruined as e:
                    (folder_out / "report.json").unlink(missing_ok=True)
                    folder_out.mkdir(parents=True, exist_ok=True)
                    (folder_out / RUINED).write_text(f"{e}\n", encoding="utf-8")
                    print(f"ruined {folder.name}: {e}")
            else:
                mc_runs.run_options(manifest, args.paths, 0, 20., OPTIONS_TODAY)
        if "xsection" in args.engines:
            only = [] if args.only is None else ["--only", *args.only]
            subprocess.run([sys.executable, str(ROOT / "strategies" / "xs" / "run_catalog.py"), "--paths",
                            str(args.xs_paths), "--slow-paths", str(args.xs_slow_paths), "--slow", *args.xs_slow,
                            *only], check=True)
        print(f"runs took {time.perf_counter() - started:.0f}s")
    for folder, manifest, engine in todo + ([(None, mc_runs.BENCHMARK, "harness")] if "benchmark" in args.engines else []):
        if report_path(manifest, engine).exists():
            r = json.loads(report_path(manifest, engine).read_text(encoding="utf-8"))
            check(r, engine)
    missing = write_index(runs, skipped)
    for name, old, new in flags(runs, headlines):
        print(f"flag {name}: old headline CAGR {old:.1%}, new {new:.1%}")
    print(f"{len({f for f, _, _ in runs})} folders tested in {len(runs)} runs, {len(skipped)} skipped, "
          f"{len(missing)} without a report: {' '.join(missing)}")


if __name__ == "__main__":
    main()
