# cat-3.12-two-moving-averages-long-short

## Monte Carlo max drawdown

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 12.0% (11th pct) | 10.0% | 18.5% | 33.8% | 40.8% | 41.1% / 10.5% / 0.0% | 706 / 1257 | -25.8% / 3.4% / 45.4% |
| benchmark | 10.2% (27th pct) | 7.3% | 13.3% | 24.3% | 29.3% | 15.1% / 0.9% / 0.0% | 324 / 900 | 3.0% / 41.1% / 87.4% |

## Walk-forward folds

| fold | return | benchmark | max DD | fills |
|---|---|---|---|---|
| 2016-07-01 | -2.10% | 3.39% | -3.9% | 4 |
| 2017-07-01 | 1.35% | 5.28% | -3.1% | 5 |
| 2018-07-01 | 2.42% | -3.51% | -6.2% | 5 |
| 2019-07-01 | -3.12% | 4.77% | -8.7% | 5 |
| 2020-07-01 | -3.17% | 9.69% | -11.7% | 7 |
| 2021-07-01 | 0.70% | 5.98% | -5.2% | 5 |
| 2022-07-01 | -1.71% | 0.58% | -5.4% | 5 |
| 2023-07-01 | 2.67% | 4.20% | -4.4% | 5 |
| 2024-07-01 | 3.01% | 4.03% | -6.6% | 4 |
| 2025-07-01 | 3.01% | 5.23% | -3.7% | 3 |

Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail (Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.
