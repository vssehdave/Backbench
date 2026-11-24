# bench-buy-and-hold-spy

## Monte Carlo max drawdown

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 10.2% (27th pct) | 7.3% | 13.3% | 24.3% | 29.3% | 15.1% / 0.9% / 0.0% | 324 / 900 | 3.0% / 41.1% / 87.4% |
| benchmark | 10.2% (27th pct) | 7.3% | 13.3% | 24.3% | 29.3% | 15.1% / 0.9% / 0.0% | 324 / 900 | 3.0% / 41.1% / 87.4% |

## Walk-forward folds

| fold | return | benchmark | max DD | fills |
|---|---|---|---|---|
| 2016-07-01 | 3.39% | 3.39% | -2.5% | 1 |
| 2017-07-01 | 5.28% | 5.28% | -1.1% | 1 |
| 2018-07-01 | -3.51% | -3.51% | -10.2% | 1 |
| 2019-07-01 | 4.77% | 4.77% | -3.4% | 1 |
| 2020-07-01 | 9.69% | 9.69% | -4.9% | 1 |
| 2021-07-01 | 5.98% | 5.98% | -3.1% | 1 |
| 2022-07-01 | 0.58% | 0.58% | -6.9% | 1 |
| 2023-07-01 | 4.20% | 4.20% | -6.0% | 1 |
| 2024-07-01 | 4.03% | 4.03% | -4.7% | 1 |
| 2025-07-01 | 5.23% | 5.23% | -2.6% | 1 |

Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail (Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.
