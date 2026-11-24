# 5-minute opening range breakout, monthly top-20 liquid stocks

Run: `python strategies/intraday/orb/run.py` (writes `results.json`). Offline tests: `test_intraday.py`.

## Rules
- Opening range: high and low of the five 09:30-09:34 minute bars (all five must exist).
- Trigger: a minute bar CLOSE above the high (long) or below the low (short), first checked on the 09:35 bar. Only
  closed bars are used. Fill: the NEXT minute's open plus or minus slippage, never the range price.
- Stop: the opposite side of the range, checked from the fill bar (a bar opening through the stop fills at its open).
- Exit: open of the 15:55 bar (12:55 on half days), or the last bar's close if missing. One trade per stock per day.
- Size: risk 1% of start-of-day equity over the stop distance, gross notional capped at 4x equity, in entry order.
  Fees `harness.fees` on both sides; slippage 0/2/5 bps per side (2 bps base).
- Shorts: reported both ways, long-short and long-only.

## Universe (no hindsight in selection)
A fixed list of 103 large US common stocks, `intraday.CANDIDATES`, written before any result was seen. Each month the
top 20 by prior-month raw dollar volume (needs 80% of that month's sessions). Limitation: the list is from what I knew
of 2020 large caps, so it has survivorship bias. 60 distinct stocks were selected over 1,660 stock-months.

## Data (2020-01-02 to 2026-11-20, 1,732 sessions)
13.4M stored minute bars, 560 MB cache, 2,782 requests, about 1.6 hours of summed fetch time, 21 minutes wall with four
threads. Only selected stock-months are fetched.

## Results (start equity 100,000)
| Run | CAGR | Sharpe | Max DD | Win rate | Avg trade | Trades/day | Cost drag/yr |
|---|---|---|---|---|---|---|---|
| Long-short 0 bps | 38.4% | 0.84 | -68.2% | 37.2% | $66 (-23 bps unweighted) | 7.3 | 10.5% |
| Long-short 2 bps | -22.7% | -0.14 | -90.2% | 36.4% | -$6 | 7.4 | 66.9% |
| Long-short 5 bps | -73.8% | -2.48 | -100% | 32.1% | -$15 | 3.8 | 157% |
| Long-only 0 bps | -4.8% | 0.24 | -74.5% | 38.0% | -$2 | 7.0 | 13.4% |
| Long-only 2 bps | -67.3% | -1.49 | -100% | 34.9% | -$10 | 6.1 | 75.1% |
| SPY | 13.1% | 0.72 | -33.8% | | | | |
| Equal-weight universe | 18.6% | 0.79 | -37.4% | | | | |

Yearly, long-short at 2 bps: 2020 -46%, 2021 +19%, 2022 +32%, 2023 -8%, 2024 -45%, 2025 -21%, 2026 -51%.
SPY: 17.4%, 28.6%, -18.2%, 26.2%, 24.9%, 17.7%, 2.0%.

## Reading
Only the zero-slippage long-short run beats the benchmarks, and it is not credible: the mean per-trade return is
negative, the profit comes from a few tight-range trades with very large share counts, and 0 bps ignores the spread.
With any slippage the strategy loses. Once equity collapses, sized trades shrink to nothing, so trade counts at 5 bps
are not comparable.
