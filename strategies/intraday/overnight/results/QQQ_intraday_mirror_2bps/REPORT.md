# intraday-overnight QQQ_intraday_mirror_2bps

![Growth of 10,000 and drawdown](equity.svg)

## Performance

2016-01-04 to 2026-11-20, 2738 sessions chained, zero risk-free rate, 252 sessions a year (CAGR from the session count). Sortino uses downside deviation below 0. Beta and annualized alpha are a CAPM regression of daily returns on SPY, whatever the headline benchmark.

| series | CAGR | Sharpe | Sortino | volatility | max DD | beta vs SPY | alpha vs SPY (annual) |
|---|---|---|---|---|---|---|---|
| strategy | -6.5% | -0.29 | -0.40 | 17.5% | -53.3% | 0.71 | -15.4% |
| SPY | 13.7% | 0.82 | 1.15 | 17.5% | -33.8% | 1.00 | +0.0% |

## Monte Carlo max drawdown

B: block bootstrap of the daily returns; 1000 paths, seed 0, mean block 20.0. Max drawdown is on the one continuous backtest.

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 53.3% (28th pct) | 35.3% | 62.5% | 82.0% | 87.4% | 100.0% / 98.8% / 77.1% | 2483 / 2736 | -78.8% / -51.4% / 13.3% |
| benchmark (SPY) | 33.8% (59th pct) | 19.3% | 32.0% | 48.1% | 57.1% | 93.0% / 57.0% / 3.3% | 530 / 1313 | 79.9% / 309.6% / 845.8% |

## Walk-forward folds

| fold | return | benchmark | max DD | fills |
|---|---|---|---|---|
| full period | -51.62% | 304.15% | -53.3% | 5474 |

Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail (Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.
