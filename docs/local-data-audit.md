# Existing QQQ and TQQQ intraday data

The VWAP TT collection contains one-minute OHLCV aggregates. They support research into signals calculated at a completed minute or session close. Individual prints, bid/ask quotes, trade conditions and exchange/receipt timestamps are absent. Bar-volume weighting yields only an approximation of trade-level VWAP unless a vendor supplies actual per-bar turnover or per-bar VWAP.

| Data | Observed range (file-local clock) | Interpretation |
|---|---|---|
| `QQQ_0.csv` | 2008-05-05 09:30 to 2026-05-15 15:59 | Symbol column and one-minute OHLCV. The file has 98,100 rows on 252 dates in 2016. |
| `Backtest/TQQQ_1min_RTH.csv` | 2018-01-02 09:30 to 2026-05-11 12:10 | 815,414 rows on 2,100 dates. Symbol comes from the filename. The final session ends midday. |
| `0.csv`, `6.csv`, `2020-22.csv`, `2023-25.csv`, `Backtest/TQQQ_1min_RTH_2025-2026.csv` | Subsets of the preceding TQQQ range | `0.csv` is byte-identical to the canonical TQQQ file. Hashes of its year-filtered rows including headers exactly match each of the four remaining files. Import one canonical source. |
| `Backtest/trades_base_TQQQ.csv`, `VIX_History.csv` | Strategy output and daily index history | Simulated entry/exit records and daily OHLC, respectively. Earlier simulated entries provide no underlying market observations. |

## Timestamps and execution

The timestamps lack UTC offsets. The preparation script describes regular hours in Eastern time. Most complete sessions span 09:30 through 15:59, consistent with start-labelled one-minute bars. Eighteen TQQQ sessions end at 13:00 with 211 rows. Confirm session-boundary and auction conventions against exchange calendars and source documentation. Time-zone intent and a suggestive clock pattern alone cannot establish when a record became observable.

For research assume a minute close becomes available no earlier than the end of its interval. Use a subsequent executable price and model dissemination/order latency when needed. Avoid same-bar close fills, inferred within-bar price ordering, spreads inferred from highs/lows, and using today's complete volume before the bar ends. A daily adapter should aggregate within a validated trading session and report truncated sessions.

## Coverage checks

Both primary files were scanned in full for timestamp order, repeated minutes, nonfinite values, inconsistent OHLC bounds and negative volume. Internal gaps count absent clock minutes strictly between consecutive rows on the same date. They exclude overnight spans and unobserved entire sessions; legitimate halts can also create gaps. Compare missing observations against an exchange calendar and halt records before imputing anything.

TQQQ had 69 internal gaps spanning 135 minutes. Its prices and volumes passed the above checks, with strictly increasing timestamps and positive volume throughout. Original vendor, adjustments, split-volume convention, licensing and publication delays are undocumented. Use point-in-time unadjusted prices with corporate actions before judging per-share commissions, dollar thresholds, or tradable quantities. Keep raw files outside Git.

QQQ had 1,761,078 strictly ordered rows on 4,536 dates, all labelled QQQ, with 167 internal gaps spanning 1,079 minutes. OHLC bounds and finite-value checks passed. One bar recorded zero volume. The sample predates 2016 and supports minute-level research across that year. TQQQ requires a separate 2016–2017 backfill for corresponding minute coverage. Both require a trade/quote source for tick-level work.

## Snapshot identity

SHA-256 of canonical TQQQ: `8719950fa937552484f46d92606851bc784762eb808efad1a5c4fed077b43b83`.
SHA-256 of canonical QQQ: `0404adf376ff73f2c05711204ade94fe9820827742801926ef6cf930558458d0`.
