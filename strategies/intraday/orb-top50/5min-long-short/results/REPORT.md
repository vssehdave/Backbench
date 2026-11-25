# intraday-orb-top50-5min-long-short

5-minute opening range breakout, long-short, on the monthly point-in-time top 50 S&P 500 stocks by market cap, 2020-01-02 to 2026-11-20. Fixed 1% risk per trade, each position capped at equity / 50 so gross never exceeds equity. IBKR fees plus per-side slippage.

| slippage per side | CAGR | Sharpe | max DD | trades | win rate | avg trade bps | max position % equity |
|---|---|---|---|---|---|---|---|
| 0 bps | -41.8% | -11.76 | -97.6% | 45785 | 29.0% | -49.2 | 2.0 |
| 2 bps | -43.1% | -12.14 | -97.9% | 40094 | 27.4% | -59.0 | 2.0 |
| 5 bps | -44.0% | -12.59 | -98.2% | 34115 | 24.9% | -71.4 | 2.0 |

Trade logs (2 bps run): trades_best_day.md, trades_worst_day.md, trades_random_day.md (and .csv), trades_all.csv.
