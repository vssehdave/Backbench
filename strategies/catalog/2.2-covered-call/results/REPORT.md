# cat-2.2-covered-call-options

## Monte Carlo max drawdown

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 16.3% (67th pct) | 7.0% | 14.1% | 24.5% | 29.1% | 14.7% / 0.8% / 0.0% | 192 / 510 | 0.9% / 34.5% / 76.6% |
| benchmark | 18.5% (61th pct) | 9.3% | 16.6% | 28.2% | 33.3% | 27.4% / 2.8% / 0.0% | 208 / 530 | -0.4% / 41.9% / 102.6% |

## Walk-forward folds

| fold | return | benchmark | max DD | fills |
|---|---|---|---|---|
| full period | 33.72% | 41.48% | -16.3% | 69 |

Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail (Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.
