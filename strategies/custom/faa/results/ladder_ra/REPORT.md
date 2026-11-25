# ladder_ra

![Growth of 10,000 and drawdown](equity.svg)

## Performance

2016-06-01 to 2026-10-30, 2620 sessions chained, zero risk-free rate, 252 sessions a year (CAGR from the session count). Sortino uses downside deviation below 0. Beta and annualized alpha are a CAPM regression of daily returns on SPY, whatever the headline benchmark.

| series | CAGR | Sharpe | Sortino | volatility | max DD | beta vs SPY | alpha vs SPY (annual) |
|---|---|---|---|---|---|---|---|
| strategy | 8.7% | 0.80 | 1.10 | 11.2% | -19.6% | 0.39 | +2.9% |
| SPY | 14.9% | 0.88 | 1.24 | 17.5% | -33.8% | 1.00 | +0.0% |

## Monte Carlo max drawdown

A: path rerun on jointly bootstrapped dates; 200 paths, seed 0, mean block 20.0. Max drawdown is on the one continuous backtest.

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 19.6% (24th pct) | 15.0% | 24.5% | 40.1% | 48.6% | 74.0% / 30.0% / 1.0% | 686 / 1718 | 11.6% / 122.8% / 346.3% |
| benchmark (SPY) | 33.8% (60th pct) | 17.0% | 31.6% | 41.7% | 48.9% | 86.0% / 52.5% / 0.5% | 464 / 990 | 106.7% / 333.6% / 822.6% |

## Walk-forward folds

| fold | return | benchmark | max DD | fills |
|---|---|---|---|---|
| 2016-06-01 | 137.16% | 324.16% | -19.6% | 431 |

Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail (Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.
