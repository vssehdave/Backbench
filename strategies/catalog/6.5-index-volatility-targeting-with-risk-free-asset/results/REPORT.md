# cat-6.5-index-volatility-targeting

## Monte Carlo max drawdown

A: path rerun on bootstrapped bars; 1000 paths, seed 0, mean block 20.0. Max drawdown is on the forward windows chained into one equity curve per path; windows are the six months after each selection half, 12-month steps, so the gaps between them are not in the curve.

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 6.6% (20th pct) | 5.4% | 8.5% | 14.7% | 18.4% | 0.8% / 0.0% / 0.0% | 350 / 925 | 1.7% / 26.3% / 54.0% |
| benchmark | 10.2% (27th pct) | 7.3% | 13.3% | 24.3% | 29.3% | 15.1% / 0.9% / 0.0% | 324 / 900 | 3.0% / 41.1% / 87.4% |
| benchmark full history (mode B) | 34.2% (60th pct) | 18.5% | 31.7% | 46.8% | 53.6% | 91.6% / 56.3% / 2.8% | 508 / 1232 | 61.0% / 250.5% / 601.6% |

## Walk-forward folds

| fold | return | benchmark | max DD | fills |
|---|---|---|---|---|
| 2016-07-01 | 2.76% | 3.39% | -2.5% | 4 |
| 2017-07-01 | 5.19% | 5.28% | -1.1% | 3 |
| 2018-07-01 | -0.21% | -3.51% | -4.9% | 6 |
| 2019-07-01 | 4.05% | 4.77% | -3.4% | 5 |
| 2020-07-01 | 4.17% | 9.69% | -3.1% | 15 |
| 2021-07-01 | 4.16% | 5.98% | -3.1% | 6 |
| 2022-07-01 | 0.43% | 0.58% | -2.0% | 12 |
| 2023-07-01 | 3.48% | 4.20% | -6.0% | 3 |
| 2024-07-01 | 2.73% | 4.03% | -4.1% | 7 |
| 2025-07-01 | 3.53% | 5.23% | -1.7% | 12 |

Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail (Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.
