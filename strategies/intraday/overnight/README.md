# Overnight only (buy official close, sell next official open)

Run: `python strategies/intraday/overnight/run.py` (writes `results.json`). Offline tests: `test_intraday.py`.

## Rules
- Buy at the day's official close (SIP 1Day bar, closing auction), sell at the next session's official open (SIP 1Day
  open). Nothing is held in regular hours. Fully invested, one round trip per session.
- Mirror: buy the official open, sell the official close. Benchmark: buy and hold on the same sessions.
- Sets: SPY, QQQ, and the monthly top-20 stock universe from the ORB strategy (equal weight, symbols picked from the
  prior month, so stocks start 2016-02). Period 2016-01-04 to 2026-11-20 (last full session; SIP is refused for today).
- Fees: `harness.fees` (IBKR style) on both sides. Slippage per side: 0, 2, 5 bps (2 bps is the base case).
- The overnight return is the auction open over the previous auction close, adjusted for splits and dividends.

## Extended-hours variant (lower quality)
SPY and QQQ only, 2016 to 2025. Buy the last post-close bar's close (16:00-20:00, to 17:00 on half days), sell the last
pre-market bar's close (04:00-09:30). Thin prints, a bar close stands in for a fill, no spread beyond the slippage
sweep. On 369 (SPY) and 399 (QQQ) nights the last post-close bar was over 5 minutes before the end of the window.

## Results (full tables and yearly returns in `results.json`)
| Set | Buy and hold CAGR / Sharpe / maxDD | Overnight 0 bps | Overnight 2 bps | Overnight 5 bps | Mirror 0 bps | Mirror 2 bps |
|---|---|---|---|---|---|---|
| SPY | 13.7% / 0.82 / -33.8% | 8.0% / 0.74 / -32.7% | -2.4% / -0.16 / -37.8% | -16.8% | 2.7% / 0.27 | -7.3% |
| QQQ | 17.9% / 0.85 / -35.0% | 10.4% / 0.80 / -27.5% | -0.2% / 0.05 / -36.3% | -14.7% | 3.5% / 0.29 | -6.5% |
| Stocks20 | 20.2% / 0.92 / -37.4% | 8.1% / 0.61 / -31.2% | -12.8% / -0.91 / -77.4% | -35.8% | -18.3% | -33.3% |

SPY overnight at 0 bps: win rate 56.4%, average trade 3.3 bps, 1 trade per day, fee drag 1.2% a year. Each extra 1 bps
per side costs about 5% a year, so the edge (about 3 to 4 bps a night) is gone at 2 bps per side. Extended hours at
0/2/5 bps, CAGR: SPY 6.6% / -3.7% / -17.8%, QQQ 7.2% / -3.1% / -17.2%; no better than the auction version.

## Caveats
Retail accounts need MOC/MOO orders to get auction prints, which carry their own costs, so 0 bps is an upper bound.
Stocks20 at 5 bps loses nearly everything and stops trading as equity nears zero.
