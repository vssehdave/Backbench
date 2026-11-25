# intraday-orb-old-5min-top20-capped

The old strategies/intraday/orb setup (5-minute range, long-short, monthly top 20 by dollar volume from intraday.CANDIDATES) re-run with each position capped at equity / 20, so gross never exceeds equity. Compare with strategies/intraday/orb (uncapped, up to 4x).

| slippage per side | CAGR | Sharpe | max DD | trades | win rate | avg trade bps | max position % equity |
|---|---|---|---|---|---|---|---|
| 0 bps | -8.3% | -0.96 | -49.8% | 34313 | 40.5% | -3.4 | 5.0 |
| 2 bps | -27.0% | -3.75 | -89.0% | 33541 | 37.7% | -14.5 | 5.0 |
| 5 bps | -43.4% | -7.70 | -98.1% | 25622 | 32.7% | -35.9 | 5.0 |

Trade logs (2 bps run): trades_best_day.md, trades_worst_day.md, trades_random_day.md (and .csv), trades_all.csv.
