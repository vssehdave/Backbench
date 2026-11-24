# xs_momentum_12_1

## Monte Carlo max drawdown

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 30.2% (97th pct) | 8.1% | 15.3% | 27.9% | 34.7% | 27.5% / 3.5% / 0.5% | 528 / 1044 | -12.7% / 15.1% / 61.4% |
| benchmark (SPY) | 19.3% (29th pct) | 13.8% | 23.1% | 39.0% | 50.9% | 67.5% / 29.0% / 1.5% | 301 / 747 | 7.1% / 103.5% / 228.6% |

## Walk-forward folds

| fold | return | benchmark | max DD | fills |
|---|---|---|---|---|
| 2016-07-01 | 0.00% | 7.88% | 0.0% | 0 |
| 2017-07-03 | 0.10% | 11.51% | -6.9% | 730 |
| 2018-07-02 | 1.70% | -6.88% | -4.9% | 725 |
| 2019-07-01 | -4.09% | 10.86% | -12.1% | 716 |
| 2020-07-01 | -13.09% | 22.14% | -21.0% | 709 |
| 2021-07-01 | -2.67% | 11.71% | -6.6% | 751 |
| 2022-07-01 | 3.47% | 2.26% | -7.6% | 690 |
| 2023-07-03 | -3.66% | 8.04% | -7.3% | 729 |
| 2024-07-01 | 1.83% | 8.39% | -5.6% | 724 |
| 2025-07-01 | 5.25% | 11.00% | -4.6% | 744 |

Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail (Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.
