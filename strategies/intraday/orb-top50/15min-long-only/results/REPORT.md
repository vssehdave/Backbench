# intraday-orb-top50-15min-long-only

15-minute opening range breakout, long-only, on the monthly point-in-time top 50 S&P 500 stocks by market cap, 2020-01-02 to 2026-11-20. Fixed 1% risk per trade, each position capped at equity / 50 so gross never exceeds equity. IBKR fees plus per-side slippage.

| slippage per side | CAGR | Sharpe | max DD | trades | win rate | avg trade bps | max position % equity |
|---|---|---|---|---|---|---|---|
| 0 bps | -24.7% | -5.39 | -85.8% | 47994 | 36.3% | -24.1 | 2.0 |
| 2 bps | -32.7% | -8.06 | -93.5% | 42627 | 31.5% | -38.4 | 2.0 |
| 5 bps | -37.4% | -10.17 | -96.0% | 35881 | 27.6% | -54.1 | 2.0 |

Trade logs (2 bps run): trades_best_day.md, trades_worst_day.md, trades_random_day.md (and .csv), trades_all.csv.
