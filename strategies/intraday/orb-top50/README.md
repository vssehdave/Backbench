# Opening range breakout, 5/10/15-minute ranges, monthly top-50 S&P 500 stocks

Run from the repo root: `python strategies/intraday/orb-top50/run.py` (about 14 minutes with a warm minute-bar cache;
needs Alpaca keys in `.env` only for bars not yet cached, and the EDGAR cache from `python fetch_edgar.py`). Writes
`results.json`, `results/REPORT.md` (every table) and one folder per run. Offline tests: `test_orb.py`.

## Rules
- Same as `../orb`: the opening range is the high and low of the first 5, 10 or 15 one-minute bars (all must exist).
  Trigger: a bar CLOSE through the range, first checked on the bar right after it. Fill: the next bar's open plus or
  minus slippage. Stop: the opposite side of the range. Exit: open of the 15:55 bar (12:55 on half days).
- Long-short and long-only, each at 0, 2 and 5 bps slippage per side, plus `harness.fees` (IBKR, 1 USD minimum).
- Sizing: 1% of start-of-day equity at risk over the stop distance, then each position capped at equity / 50, and
  leverage capped at 1, so gross never exceeds equity. The cap binds on almost every trade, so in practice every
  position is about 2% of equity.

## Universe (point in time)
Each month, the 50 largest S&P 500 members by market cap on the last session of the prior month. Market cap = EDGAR
shares from the latest filing dated on or before that session, times the price the way the #1-holding strategy does
it (`leader_rules.market_caps`: raw close on the filing day, carried forward with adjusted closes). 83 months,
94 distinct stocks, 4,150 stock-months. Limits:
- **Meta and Berkshire are never in the universe.** Their EDGAR records carry no usable share-count facts, so they
  cannot be ranked. GOOG represents Alphabet (both classes summed).
- 125 symbols that were members at some point since 2016 have no EDGAR facts (mostly delisted or renamed tickers), so
  a large company that later left the index could be missed. Sectors are today's GICS labels.

## Results, 2020-01-02 to 2026-11-20 (1,732 sessions, start equity 100,000)
Every capped run loses money at every cost level. See each run folder for its table and trade logs.

| range | version | 0 bps CAGR / Sharpe / max DD / win | 2 bps | 5 bps |
|---|---|---|---|---|
| 5 | long-short | -41.8% / -11.8 / -97.6% / 29.0% | -43.1% / -12.1 / -97.9% / 27.4% | -44.0% / -12.6 / -98.2% / 24.9% |
| 5 | long-only | -32.7% / -7.8 / -93.5% / 31.5% | -37.2% / -9.7 / -96.0% / 28.5% | -39.5% / -10.8 / -96.8% / 25.8% |
| 10 | long-short | -41.6% / -11.5 / -97.5% / 30.5% | -42.9% / -11.8 / -97.9% / 28.5% | -44.0% / -12.3 / -98.1% / 25.8% |
| 10 | long-only | -27.9% / -6.2 / -89.5% / 34.6% | -34.7% / -8.7 / -94.7% / 30.4% | -38.3% / -10.4 / -96.4% / 27.2% |
| 15 | long-short | -41.2% / -11.2 / -97.4% / 31.3% | -42.5% / -11.5 / -97.8% / 29.3% | -43.8% / -12.2 / -98.1% / 26.4% |
| 15 | long-only | -24.7% / -5.4 / -85.8% / 36.3% | -32.7% / -8.1 / -93.5% / 31.5% | -37.4% / -10.2 / -96.0% / 27.6% |

SPY buy and hold over the same sessions: 13.1% CAGR, Sharpe 0.72, max DD -33.8%.

Why so bad: before any fee the trades lose about 4 to 5 bps each (fixed 10,000 USD per trade, below), and a 2,000 USD
position pays the 1 USD minimum commission each side, about 10 bps round trip; as equity shrinks the positions shrink
and the minimum fee weighs more. With positions capped at equity / 10 instead (fewer, larger trades) the 2 bps runs
are still -23% to -49% a year (REPORT.md).

### The sizing cap on its own: old 5-minute, top-20 setup (`../orb`, folder `old-5min-top20-capped`)
| slippage | uncapped (up to 4x): CAGR / Sharpe / max DD | capped at equity / 20 |
|---|---|---|
| 0 bps | 38.4% / 0.83 / -68.2% | -8.3% / -0.96 / -49.8% |
| 2 bps | -22.7% / -0.14 / -90.2% | -27.0% / -3.75 / -89.0% |
| 5 bps | -73.8% / -2.48 / -100% | -43.4% / -7.70 / -98.1% |

The old 38% came from 4x-equity positions on tight ranges at zero cost. With no leverage it is -8.3% a year.

## Analysis: which stocks, and does it hold up
Per-stock statistics use the long-short 2 bps trades at a fixed 10,000 USD each (fees included), so every trade counts
equally. Features are known before entry: opening-range width / price, 20-day ATR / prior close, gap from prior close,
prior-month dollar volume, 1-year daily beta to SPY, prior close, and cap rank.

**Pooled:** -5.4, -5.7 and -5.6 bps per trade for the 5, 10 and 15-minute ranges (about 81,000 to 84,000 trades
each), negative in both 2020-2022 and 2023-2026.

**Top and bottom by P&L** (largely the same for all three ranges): top is TSLA by far (+13,500 to +22,200 USD), then
NVDA, PANW, AMT, KLAC, MU, AVGO, ORCL, AMD, PLTR at +1,000 to +4,400 USD; PANW, KLAC, AMT, MU and APP had under 300
trades each. Bottom is ABBV, JNJ, MRK, BAC, KO, PEP, CVX, AMGN and PG (10 and 15-minute also UNH, CSCO, MCD), at
-12,500 to -22,000 USD each.

**What the winners share:** high volatility. Against the rest, winners have about 1.5 to 2 times the ATR %,
opening-range width % and gap, beta about 1.5 to 2.0 against 0.9, and a higher price. Across stocks, P&L vs ATR % has
Spearman rho 0.65 to 0.72 and vs beta 0.67 to 0.70; dollar volume and cap rank 0.2 to 0.3. By sector, 9 to 11 of the
15 or 16 winners are Information Technology; no Consumer Staples, Financials or Utilities stock is a winner. Losers
are low-volatility defensives and banks.

**Out of sample: the winners do not hold up.**
- Stocks picked as the top 20% in 2020-2022 earned -1.9, -5.3 and -3.5 bps per trade in 2023-2026 (5, 10, 15-minute),
  against -5.5, -5.6 and -5.6 for the rest. Still a loss in every case. Only the 5-minute gap is outside chance
  (shuffle p = 0.04); 10 and 15-minute are p = 0.49 and 0.14.
- Per-stock rank correlation between the two halves is 0.14 to 0.23.
- Chance: of 85 stocks with 50+ trades, 1, 1 and 0 have t > 2. Shuffling returns among stocks within each day gives
  0.1 on average (95th percentile 1), and a binomial count gives 1.9 expected. TSLA's t (2.64 at 5 minutes) is the
  only one above the shuffle 95th percentile (2.23), and only at 5 minutes.
- Feature rules with cut points from 2020-2022: the top ATR % tercile went from -7.6 to +0.8 bps (5-minute) and -0.6
  (15-minute) in 2023-2026 (t 0.5 and -0.4), which is not distinguishable from zero and loses money after the 2 bps.
  The bottom terciles of ATR, beta and dollar volume lose consistently (t about -9 to -11).

Verdict: no selection of stocks or features found here makes this ORB profitable after costs. Volatile stocks lose
less, which matches the old result, but that is the only stable pattern and it does not turn positive.

Not covered: Monte Carlo (unmerged `research/monte-carlo` branch), borrow costs and short-sale limits, partial fills.
