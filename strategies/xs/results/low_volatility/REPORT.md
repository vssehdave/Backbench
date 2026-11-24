# xs_low_volatility

## Monte Carlo max drawdown

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 14.2% (15th pct) | 11.4% | 19.2% | 36.8% | 45.2% | 40.0% / 20.0% / 0.0% | 403 / 777 | 19.6% / 63.0% / 153.8% |
| benchmark (SPY) | 19.3% (18th pct) | 16.5% | 22.7% | 40.5% | 50.5% | 80.0% / 25.0% / 2.5% | 326 / 892 | 14.3% / 96.6% / 196.5% |

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
