# intraday-overnight stocks20_overnight_2bps

![Growth of 10,000 and drawdown](equity.svg)

## Performance

2016-02-01 to 2026-11-20, 2719 sessions chained, zero risk-free rate, 252 sessions a year (CAGR from the session count). Sortino uses downside deviation below 0. Beta and annualized alpha are a CAPM regression of daily returns on SPY, whatever the headline benchmark.

| series | CAGR | Sharpe | Sortino | volatility | max DD | beta vs SPY | alpha vs SPY (annual) |
|---|---|---|---|---|---|---|---|
| strategy | -12.8% | -0.91 | -1.17 | 14.0% | -77.4% | 0.50 | -20.2% |
| SPY | 14.2% | 0.85 | 1.19 | 17.5% | -33.8% | 1.00 | +0.0% |

## Monte Carlo max drawdown

B: block bootstrap of the daily returns; 1000 paths, seed 0, mean block 20.0. Max drawdown is on the one continuous backtest.

| series | historical max DD (pct rank) | DD p5 | p50 | p95 | p99 | P(DD>20/30/50%) | underwater sessions p50 / p95 | terminal return p5 / p50 / p95 |
|---|---|---|---|---|---|---|---|---|
| strategy | 77.4% (44th pct) | 59.3% | 78.9% | 90.2% | 93.1% | 100.0% / 100.0% / 99.0% | 2680 / 2719 | -89.3% / -76.4% / -52.8% |
| benchmark (SPY) | 33.8% (61th pct) | 18.5% | 31.9% | 45.7% | 55.2% | 90.8% / 57.5% / 2.8% | 504 / 1222 | 90.8% / 329.8% / 832.8% |

## Walk-forward folds

| fold | return | benchmark | max DD | fills |
|---|---|---|---|---|
| full period | -77.28% | 319.54% | -77.4% | 108668 |

Trade logs: trades_best_day.md, trades_worst_day.md, trades_random_day.md, trades_all.csv. Full detail (Sharpe, volatility, turnover, cost drag, abstentions, forced closes, execution stress) is in report.json.
