"""Shared helpers for strategies/custom/*: long-window metrics and a one-pass xsection run. See strategies/custom/INDEX.md."""
import math
import statistics
from datetime import date

import xsection


def metrics(dates, equity, periods=252):
    """CAGR from calendar days; volatility and Sharpe (risk-free rate 0) from per-period returns."""
    returns = [b / a - 1 for a, b in zip(equity, equity[1:])]
    years = (dates[-1] - dates[0]).days / 365.25
    sd = statistics.stdev(returns) if len(returns) > 1 else 0.
    peak, drawdown = equity[0], 0.
    for e in equity:
        peak = max(peak, e)
        drawdown = min(drawdown, e / peak - 1)
    return dict(start=str(dates[0]), end=str(dates[-1]), total_return=equity[-1] / equity[0] - 1,
                cagr=(equity[-1] / equity[0]) ** (1 / years) - 1 if equity[-1] > 0 else -1.,
                volatility=sd * math.sqrt(periods), sharpe=statistics.fmean(returns) / sd * math.sqrt(periods) if sd else None,
                max_drawdown=drawdown)


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
