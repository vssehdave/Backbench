# cat-3.12-two-moving-averages

## Monte Carlo max drawdown

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 6.9% (11th pct) | 6.1% | 10.5% | 18.6% | 23.0% | 3.0% / 0.0% / 0.0% | 424 / 1106 | -5.2% / 20.8% / 56.1% |
| benchmark | 10.2% (27th pct) | 7.3% | 13.3% | 24.3% | 29.3% | 15.1% / 0.9% / 0.0% | 324 / 900 | 3.0% / 41.1% / 87.4% |

## Walk-forward folds

| fold | return | benchmark | max DD | fills |
|---|---|---|---|---|
| 2016-07-01 | 0.67% | 3.39% | -1.6% | 3 |
| 2017-07-01 | 3.31% | 5.28% | -1.2% | 5 |
| 2018-07-01 | -0.52% | -3.51% | -2.9% | 4 |
| 2019-07-01 | 0.83% | 4.77% | -5.1% | 5 |
| 2020-07-01 | 3.24% | 9.69% | -6.8% | 7 |
| 2021-07-01 | 3.34% | 5.98% | -2.6% | 5 |
| 2022-07-01 | -0.55% | 0.58% | -4.7% | 4 |
| 2023-07-01 | 3.44% | 4.20% | -3.6% | 5 |
| 2024-07-01 | 3.52% | 4.03% | -4.0% | 4 |
| 2025-07-01 | 4.12% | 5.23% | -2.3% | 3 |

Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail (Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.
