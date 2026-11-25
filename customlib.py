"""Shared helpers for strategies/custom/*: long-window metrics and a one-pass xsection run. See strategies/custom/INDEX.md."""
import statistics
import time
from datetime import date
from pathlib import Path

import mc_runs
import montecarlo
import report
import xsection


def metrics(dates, equity, periods=252):
    """CAGR from calendar days; the rest is report.perf_metrics (risk-free rate 0, sample volatility, Sortino)."""
    returns = [b / a - 1 for a, b in zip(equity, equity[1:])]
    m = report.perf_metrics(returns, periods=periods, years=(dates[-1] - dates[0]).days / 365.25)
    m["cagr"] = m["cagr"] if equity[-1] > 0 else -1.
    return dict(m, start=str(dates[0]), end=str(dates[-1]))


def first_index(panel, day):
    return next(i for i, d in enumerate(panel.dates) if d >= day)


def run_panel(panel, decide, limits, cadence, start, end=None, cash0=100_000., costs=xsection.Costs()):
    """One continuous run from the close before `start` to the last session before `end` (default: end of panel).

    Unlike xsection.study this is a single 10-year path, not six-month test folds. Returns the report dict.
    """
    i0 = max(first_index(panel, start) - 1, 0)
    i1 = len(panel.dates) - 1 if end is None else max(i for i, d in enumerate(panel.dates) if d < end)
    run = xsection.run_window(panel, decide, None, i0, i1, limits, costs, cadence, cash0)
    dates = panel.dates[i0:i1 + 1]
    years = (dates[-1] - dates[0]).days / 365.25
    avg = statistics.fmean(run["equity"])
    spent = sum(run["costs"].values())
    return dict(metrics=metrics(dates, run["equity"]), turnover_per_year=run["traded"] / avg / years,
                costs_usd=run["costs"], costs_pct_of_avg_equity_per_year=spent / avg / years,
                decisions=len(run["decisions"]), abstentions=run["abstentions"], forced_closes=run["forced_closes"],
                names_held_avg=statistics.fmean(len(w) for _, w in run["decisions"]) if run["decisions"] else 0,
                ending_equity=run["equity"][-1], start_cash=cash0, equity=run["equity"], dates=[str(d) for d in dates],
                decision_log=run["decisions"])


def buy_hold(panel, symbol, dates_from, dates_to):
    """Adjusted-close (total return) buy and hold of one symbol over panel indexes, no costs."""
    p = panel.adj[symbol][dates_from:dates_to + 1]
    return metrics(panel.dates[dates_from:dates_to + 1], [x / p[0] for x in p])


def report_panel(folder, name, panel, make_decide, limits, cadence, start, costs=xsection.Costs(), cash0=100_000.,
                 paths=200, seed=0, block=20.):
    """Standard report for one continuous run from `start` to the end of the panel, with Monte Carlo mode A on
    jointly bootstrapped dates (strategy and SPY). Writes folder/results/<name>/ and folder/mc_results_<name>.json.

    make_decide(panel) returns a fresh decide, so stateful rules start clean and read the path they run on.
    """
    started = time.perf_counter()
    i0, i1 = max(first_index(panel, start) - 1, 0), len(panel.dates) - 1
    run = lambda p: xsection.run_window(p, make_decide(p), None, i0, i1, limits, costs, cadence, cash0)
    spy = lambda p: xsection._benchmark(p, ["SPY"], i0, i1, cash0)
    mc = montecarlo.MonteCarlo(paths, seed, block)
    mc.panel_fold(0, panel, i0, i1, {"strategy": lambda p: run(p)["equity"], "benchmark (SPY)": spy})
    real = run(panel)
    fold = dict(real, test_start=str(panel.dates[i0 + 1]), bench_equity=dict(spy=spy(panel)),
                dates=[str(d) for d in panel.dates[i0:i1 + 1]])
    result = dict(start_cash=cash0, cadence=cadence, limits=vars(limits), costs=vars(costs), costs_usd=real["costs"],
                  decisions=len(real["decisions"]), abstentions=real["abstentions"], forced_closes=real["forced_closes"],
                  fills=len(real["fills"]))
    config = dict(note="Max drawdown is on the one continuous backtest.", mode="A: path rerun on jointly bootstrapped dates",
                  paths=paths, seed=seed, mean_block=block, start=str(panel.dates[i0 + 1]), end=str(panel.dates[i1]))
    folder = Path(folder)
    return mc_runs.finish((folder / "results" / name, folder / f"mc_results_{name}.json"), "xsection", name, result,
                          report.folds_of("xsection", dict(folds=[fold])), mc.summary()["mode_a"], config, started, seed)
