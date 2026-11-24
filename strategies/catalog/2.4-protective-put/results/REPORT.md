# cat-2.4-protective-put-options

## Monte Carlo max drawdown

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 14.1% (55th pct) | 8.1% | 13.9% | 23.4% | 29.0% | 12.4% / 0.6% / 0.0% | 228 / 574 | -3.2% / 32.5% / 81.8% |
| benchmark | 18.5% (61th pct) | 9.3% | 16.6% | 28.2% | 33.3% | 27.4% / 2.8% / 0.0% | 208 / 530 | -0.4% / 41.9% / 102.6% |

## Walk-forward folds

| fold | return | benchmark | max DD | fills |
|---|---|---|---|---|
| full period | 32.48% | 41.48% | -14.1% | 69 |

Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail (Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.
