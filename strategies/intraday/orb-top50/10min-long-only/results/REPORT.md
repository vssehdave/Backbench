# intraday-orb-top50-10min-long-only

10-minute opening range breakout, long-only, on the monthly point-in-time top 50 S&P 500 stocks by market cap, 2020-01-02 to 2026-11-20. Fixed 1% risk per trade, each position capped at equity / 50 so gross never exceeds equity. IBKR fees plus per-side slippage.

| slippage per side | CAGR | Sharpe | max DD | trades | win rate | avg trade bps | max position % equity |
|---|---|---|---|---|---|---|---|
| 0 bps | -27.9% | -6.24 | -89.5% | 49344 | 34.6% | -27.3 | 2.0 |
| 2 bps | -34.7% | -8.68 | -94.7% | 43084 | 30.4% | -41.3 | 2.0 |
| 5 bps | -38.3% | -10.41 | -96.4% | 36059 | 27.2% | -55.2 | 2.0 |

Trade logs (2 bps run): trades_best_day.md, trades_worst_day.md, trades_random_day.md (and .csv), trades_all.csv.
