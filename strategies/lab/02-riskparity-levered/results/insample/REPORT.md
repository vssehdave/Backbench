# insample

![Growth of 10,000 and drawdown](equity.svg)

## Performance

2016-01-05 to 2023-12-29, 2011 sessions chained, zero risk-free rate, 252 sessions a year (CAGR from the session count). Sortino uses downside deviation below 0. Beta and annualized alpha are a CAPM regression of daily returns on SPY, whatever the headline benchmark.

| series | CAGR | Sharpe | Sortino | volatility | max DD | beta vs SPY | alpha vs SPY (annual) |
|---|---|---|---|---|---|---|---|
| strategy | 10.7% | 0.79 | 1.09 | 14.1% | -27.4% | 0.53 | +3.7% |
| SPY | 13.2% | 0.78 | 1.08 | 18.1% | -33.8% | 1.00 | +0.0% |

## Monte Carlo max drawdown

A: path rerun on jointly bootstrapped dates; 200 paths, seed 0, mean block 20.0. Max drawdown is on the one continuous backtest.

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 27.4% (56th pct) | 17.4% | 26.5% | 40.3% | 58.1% | 85.5% / 29.0% / 1.5% | 531 / 1340 | 11.1% / 114.4% / 316.2% |
| benchmark (SPY) | 33.8% (58th pct) | 16.6% | 30.9% | 50.8% | 57.9% | 89.0% / 53.5% / 5.5% | 468 / 1159 | 14.1% / 166.9% / 411.0% |

## Walk-forward folds

| fold | return | benchmark | max DD | fills |
|---|---|---|---|---|
| 2016-01-05 | 125.05% | 169.64% | -27.4% | 384 |

Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail (Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.
