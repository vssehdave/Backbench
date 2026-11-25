# intraday-orb-top50-5min-long-only

5-minute opening range breakout, long-only, on the monthly point-in-time top 50 S&P 500 stocks by market cap, 2020-01-02 to 2026-11-20. Fixed 1% risk per trade, each position capped at equity / 50 so gross never exceeds equity. IBKR fees plus per-side slippage.

| slippage per side | CAGR | Sharpe | max DD | trades | win rate | avg trade bps | max position % equity |
|---|---|---|---|---|---|---|---|
| 0 bps | -32.7% | -7.82 | -93.5% | 49477 | 31.5% | -33.3 | 2.0 |
| 2 bps | -37.2% | -9.70 | -96.0% | 42657 | 28.5% | -45.6 | 2.0 |
| 5 bps | -39.5% | -10.80 | -96.8% | 35788 | 25.8% | -58.2 | 2.0 |

Trade logs (2 bps run): trades_best_day.md, trades_worst_day.md, trades_random_day.md (and .csv), trades_all.csv.
