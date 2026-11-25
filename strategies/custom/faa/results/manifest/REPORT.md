# custom_faa

## Monte Carlo max drawdown

A: path rerun on jointly bootstrapped dates; 200 paths, seed 0, mean block 20.0. Max drawdown is on the forward windows chained into one equity curve per path; the gaps between windows (12-month steps) are not in the curve.

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 14.7% (44th pct) | 9.2% | 15.7% | 28.5% | 35.4% | 26.5% / 3.5% / 0.5% | 440 / 1011 | -4.7% / 33.3% / 86.6% |
| benchmark (SPY) | 19.3% (29th pct) | 13.8% | 23.1% | 39.0% | 50.9% | 67.5% / 29.0% / 1.5% | 301 / 747 | 7.1% / 103.5% / 228.6% |

## Walk-forward folds

| fold | return | benchmark | max DD | fills |
|---|---|---|---|---|
| 2016-07-01 | -7.69% | 7.88% | -9.7% | 25 |
| 2017-07-03 | 8.10% | 11.51% | -2.8% | 23 |
| 2018-07-02 | -4.44% | -6.88% | -7.5% | 21 |
| 2019-07-01 | 4.48% | 10.86% | -1.7% | 24 |
| 2020-07-01 | 13.68% | 22.14% | -4.9% | 25 |
| 2021-07-01 | -3.08% | 11.71% | -7.1% | 24 |
| 2022-07-01 | -2.53% | 2.26% | -5.2% | 12 |
| 2023-07-03 | -3.00% | 8.04% | -5.7% | 19 |
| 2024-07-01 | 0.25% | 8.39% | -6.3% | 23 |
| 2025-07-01 | 10.54% | 11.00% | -3.9% | 22 |

Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail (Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.
