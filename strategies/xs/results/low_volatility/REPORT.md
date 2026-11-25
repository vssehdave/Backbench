# xs_low_volatility

## Monte Carlo max drawdown

A: path rerun on jointly bootstrapped dates; 200 paths, seed 0, mean block 20.0. Max drawdown is on the forward windows chained into one equity curve per path; the gaps between windows (12-month steps) are not in the curve.

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 14.2% (30th pct) | 10.6% | 18.1% | 36.7% | 43.3% | 40.0% / 22.5% / 0.5% | 281 / 824 | 11.5% / 67.4% / 152.3% |
| benchmark (SPY) | 19.3% (29th pct) | 13.8% | 23.1% | 39.0% | 50.9% | 67.5% / 29.0% / 1.5% | 301 / 747 | 7.1% / 103.5% / 228.6% |

## Walk-forward folds

| fold | return | benchmark | max DD | fills |
|---|---|---|---|---|
| 2016-07-01 | 0.00% | 7.88% | 0.0% | 0 |
| 2017-07-03 | 8.49% | 11.51% | -1.6% | 622 |
| 2018-07-02 | 0.35% | -6.88% | -11.6% | 637 |
| 2019-07-01 | 6.88% | 10.86% | -3.6% | 619 |
| 2020-07-01 | 13.24% | 22.14% | -6.5% | 622 |
| 2021-07-01 | 12.68% | 11.71% | -6.1% | 644 |
| 2022-07-01 | 2.68% | 2.26% | -14.2% | 625 |
| 2023-07-03 | 1.51% | 8.04% | -8.8% | 634 |
| 2024-07-01 | 9.13% | 8.39% | -6.8% | 640 |
| 2025-07-01 | -1.94% | 11.00% | -5.5% | 630 |

Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail (Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.
