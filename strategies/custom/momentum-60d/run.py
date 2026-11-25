"""Run 60-day momentum on SPY, QQQ and BTC through the harness replay. Usage: python strategies/custom/momentum-60d/run.py"""
import json
import sys
import time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path[:0] = [str(ROOT), str(Path(__file__).parent)]
import customlib
import harness
import mc_runs
import money
import montecarlo

BUFFER = 0.98  # headroom for the open gap and fees: a fill that cannot be paid is rejected by replay
START = 10000.
FROM = date(2017, 1, 1)  # load_rows fetches 12 months before this, so the rows start 2016-01 (first Alpaca SIP year)
SEGMENT = 21   # sessions between equity-based re-sizing


def simulate(rows, manifest, rule, level=60):
    """Chained replays. The share target is fixed while long (no ratchet) and re-sized to equity every SEGMENT rows.

    money.Plugin sizes against START_CASH at each close, which stops compounding over a 10-year run, so it is bypassed.
    Returns equity per row, fills, and the number of segment ends where the shares held differed from the target.
    """
    spot = money.spot_costs(manifest)
    lot = spot.lot_size if spot else 1
    state, history, equity, fills, unfilled = (START, 0), [], [], [], 0
    for k in range(0, len(rows), SEGMENT):
        chunk = rows[k:k + SEGMENT]
        budget = state[0] + state[1] * lot * (history[-1] if history else 0)
        held = dict(target=0, resize=True)

        def strategy(past, lvl):
            flag = rule(past, lvl)
            if not flag:
                held["target"] = 0
            elif held["target"] == 0 or held["resize"]:
                held["target"] = int(BUFFER * budget / (lot * past[-1]))
            held["resize"] = False
            return held["target"]

        state, part, got = harness.replay(chunk, strategy, level, state, history, spot=spot)
        history += [c for _, _, c in chunk]
        equity += part
        fills += got
        unfilled += state[1] != held["target"]
    return equity, fills, unfilled


def metrics_for(rows, equity, fills):
    dates = [d for d, _, _ in rows]
    m = customlib.metrics(dates, [START] + equity)  # equity starts at the 10000 cash
    avg = sum(equity) / len(equity)
    years = (dates[-1] - dates[0]).days / 365.25
    fee = sum(f["commission"] + f["regulatory"] for f in fills)
    traded = sum(abs(f["quantity"] * f["price"]) for f in fills)
    return dict(m, fills=len(fills), turnover_per_year=traded / avg / years, fees_usd=fee,
                fees_pct_of_avg_equity_per_year=fee / avg / years)


def hold(rows, manifest):
    """Buy and hold through the same replay and costs: one fill at the first open, no re-sizing."""
    spot = money.spot_costs(manifest)
    lot = spot.lot_size if spot else 1
    target = int(BUFFER * START / (lot * rows[0][1]))
    return harness.replay(rows, lambda past, level: target, 0, (START, 0), [], spot=spot)[1:]


def write_standard_report(name, manifest, rows, spy, paths=1000, seed=0, block=20.):
    """results/<name>/ via report.write_report. rows[0] only anchors the bootstrap price, so the run is rows[1:].

    Monte Carlo mode A reruns momentum and buy and hold on the same bootstrapped bars.
    """
    started = time.perf_counter()
    rule = __import__("mom60_rules").decide
    runs = {"strategy": lambda r: [START] + simulate(r, manifest, rule)[0],
            f"benchmark ({name} buy and hold)": lambda r: [START] + hold(r, manifest)[0]}
    mc = montecarlo.MonteCarlo(paths, seed, block)
    for key, run in runs.items():
        mc.rows_fold(key, 0, rows, rows[:1], rows[1:], run)
    equity, fills, _ = simulate(rows[1:], manifest, rule)
    fold = dict(label="full period", dates=[str(d) for d, _, _ in rows[1:]], equity=[START] + equity,
                bench=[START] + hold(rows[1:], manifest)[0], fills=[dict(f, symbol=name) for f in fills], borrow={},
                bench_name=f"{name} buy and hold")
    config = dict(note="Max drawdown is on the one continuous backtest.", mode="A: path rerun on bootstrapped bars",
                  paths=paths, seed=seed, mean_block=block, start=str(rows[1][0]), end=str(rows[-1][0]))
    here = Path(__file__).parent
    mc_runs.finish((here / "results" / name, here / f"mc_results_{name}.json"), "harness", manifest["id"],
                   dict(fills=len(fills)), [fold], mc.summary()["mode_a"], config, started, seed, spy=spy,
                   periods=365 if manifest["calendar"] == "utc24" else 252)


def main():
    out, rows_by = {}, {}
    for name in sys.argv[1:] or ("SPY", "QQQ", "BTC"):
        manifest = money.load_manifest(Path(__file__).with_name(f"manifest-{name}.json"))
        rows, source, quality = money.load_rows(manifest, FROM, date(2026, 1, 1))
        rows_by[name] = rows
        equity, fills, unfilled = simulate(rows, manifest, __import__("mom60_rules").decide)
        h_equity, h_fills = hold(rows, manifest)
        out[name] = dict(source=source, rows=len(rows), momentum=metrics_for(rows, equity, fills), segments_with_unfilled_target=unfilled,
                         buy_hold_price_only=metrics_for(rows, h_equity, h_fills),
                         cash=dict(cagr=0., volatility=0., sharpe=None, max_drawdown=0.))
    Path(__file__).with_name("results.json").write_text(json.dumps(out, indent=1, default=str), encoding="utf-8")
    spy_manifest = money.load_manifest(Path(__file__).with_name("manifest-SPY.json"))
    spy = {d: c for d, _, c in rows_by.get("SPY") or money.load_rows(spy_manifest, FROM, date(2026, 1, 1))[0]}
    for name, rows in rows_by.items():
        write_standard_report(name, money.load_manifest(Path(__file__).with_name(f"manifest-{name}.json")), rows, spy)
    for name, r in out.items():
        print(name, r["source"], r["rows"], r["segments_with_unfilled_target"])
        for k in ("momentum", "buy_hold_price_only"):
            print("  ", k, {x: round(y, 4) if isinstance(y, float) else y for x, y in r[k].items()})


if __name__ == "__main__":
    main()
