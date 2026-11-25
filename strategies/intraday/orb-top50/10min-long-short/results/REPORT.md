# intraday-orb-top50-10min-long-short

10-minute opening range breakout, long-short, on the monthly point-in-time top 50 S&P 500 stocks by market cap, 2020-01-02 to 2026-11-20. Fixed 1% risk per trade, each position capped at equity / 50 so gross never exceeds equity. IBKR fees plus per-side slippage.

| slippage per side | CAGR | Sharpe | max DD | trades | win rate | avg trade bps | max position % equity |
|---|---|---|---|---|---|---|---|
| 0 bps | -41.6% | -11.45 | -97.5% | 45764 | 30.5% | -49.1 | 2.0 |
| 2 bps | -42.9% | -11.79 | -97.9% | 39988 | 28.5% | -58.9 | 2.0 |
| 5 bps | -44.0% | -12.33 | -98.1% | 34018 | 25.8% | -71.3 | 2.0 |

Trade logs (2 bps run): trades_best_day.md, trades_worst_day.md, trades_random_day.md (and .csv), trades_all.csv.
