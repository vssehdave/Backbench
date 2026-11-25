# intraday-orb-top50-15min-long-short

15-minute opening range breakout, long-short, on the monthly point-in-time top 50 S&P 500 stocks by market cap, 2020-01-02 to 2026-11-20. Fixed 1% risk per trade, each position capped at equity / 50 so gross never exceeds equity. IBKR fees plus per-side slippage.

| slippage per side | CAGR | Sharpe | max DD | trades | win rate | avg trade bps | max position % equity |
|---|---|---|---|---|---|---|---|
| 0 bps | -41.2% | -11.22 | -97.4% | 46582 | 31.3% | -47.3 | 2.0 |
| 2 bps | -42.5% | -11.47 | -97.8% | 40599 | 29.3% | -57.1 | 2.0 |
| 5 bps | -43.8% | -12.15 | -98.1% | 34631 | 26.4% | -69.7 | 2.0 |

Trade logs (2 bps run): trades_best_day.md, trades_worst_day.md, trades_random_day.md (and .csv), trades_all.csv.
