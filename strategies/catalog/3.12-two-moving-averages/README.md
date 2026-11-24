# 3.12 Two moving averages

- Section: 3.12
- Asset class: Stocks
- Harness status: **tested**. Rule as implemented: Long when MA(10) > MA(T), flat when below, T = 30 (the paper's example values). Long-only here; a long/short variant (short when MA(10) < MA(T)) is under Results. The optional stop-loss variant is not implemented.

## Description (paper)

The simplest variant of this strategy replaces the stock price P in Eq. (321) by another moving average. That is, we have 2 moving averages with lengths T ′ and *T, where T ′ \< T (e.g., T ′ = 10 and T = 30), and the signal is given by: Signal = (

Establish long/liquidate short position if MA( *T ′) \> MA( *T) Establish short/liquidate long position if MA( *T ′) \< MA( *T) (322)

This signal can be augmented with additional "stop-loss" rules to protect realized profits. E.g., if a long position has been established, the trader can define a threshold

to liquidate the long position if the stock begins to fall (even if the shorter moving average has not crossed the longer moving average yet): Signal =         

Establish long position if MA( *T ′) \> MA( *T) Liquidate long position if P \< (1 − ∆) × P 1 Establish short position if MA( *T ′) \< MA( *T) Liquidate short position if P \> (1 + ∆) × P 1 (323)

Here ∆is some predefined percentage, e.g., ∆= 2%. So, a long position is liquidated if the current price P falls over 2% below the previous day's price P 1; and a short position is liquidated if P rises over 2% above P 1. Other variations can be used.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.12. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

Real data: SPY daily raw SIP bars from Alpaca, 2016-01-01 to 2026-01-01 (exclusive), run with `python money.py test 3.12-two-moving-averages/manifest.json --start 2016-01-01 --end 2026-01-01` (saved as `results.json`). Defaults: 20 stress paths, 10 bps shock, seed 42.

| Forward window | Selected | Strategy | Cash | Buy and hold | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 30 | 0.67% | 0.00% | 3.39% | 2+1 |
| 2017-07-01..2018-01-01 | 30 | 3.31% | 0.00% | 5.28% | 3+2 |
| 2018-07-01..2019-01-01 | 30 | -0.52% | 0.00% | -3.51% | 2+2 |
| 2019-07-01..2020-01-01 | 30 | 0.83% | 0.00% | 4.77% | 3+2 |
| 2020-07-01..2021-01-01 | 30 | 3.24% | 0.00% | 9.69% | 4+3 |
| 2021-07-01..2022-01-01 | 30 | 3.34% | 0.00% | 5.98% | 3+2 |
| 2022-07-01..2023-01-01 | 30 | -0.55% | 0.00% | 0.58% | 2+2 |
| 2023-07-01..2024-01-01 | 30 | 3.44% | 0.00% | 4.20% | 3+2 |
| 2024-07-01..2025-01-01 | 30 | 3.52% | 0.00% | 4.03% | 2+2 |
| 2025-07-01..2026-01-01 | 30 | 4.12% | 0.00% | 5.23% | 2+1 |
| **Compounded** | | **23.39%** | 0.00% | 46.79% | |

Strategy ranks above buy and hold in 1 of 10 windows; abstentions 0. Cash and buy-and-hold are the repo's own `controls:cash` and `controls:buy_and_hold` run through the same folds, fees and sizing (`../_benchmarks/`).

Read with care:
- Only the second half of each calendar year (July-December) is a forward window; the other half trains. Ten windows cover half the decade, so the compounded numbers are not a ten-year return.
- Each window is one 6-month sample, and the level is chosen per window on a 3-month selection slice, so the selected level changes.
- Prices are raw (no dividends), which understates buy-and-hold and the long legs equally.
- Signals use the prior close and fill at the next open, with the repo's IBKR fee model; position is a fixed share count of about 5,000 USD at the window's first training close (half of the 10,000 USD of cash).
- Parameters are the paper's examples where it gives them, otherwise the author's fixed choice (see Harness status), and were not changed after seeing results.

### Long/short variant

Same rule and sizing, but short (about 5,000 USD of shares) instead of flat when MA(10) < MA(T). Manifest `manifest_long_short.json` (`allow_short`, 50 bps a year borrow), rule `strategy_ls.py`, same command with that manifest, saved as `results_long_short.json`. Forced closes: 0 in every window.

| Forward window | Long/short | Long-only | Buy and hold | Fills (buys+sells) |
|---|---|---|---|---|
| 2016-07-01..2017-01-01 | -2.10% | 0.67% | 3.39% | 2+2 |
| 2017-07-01..2018-01-01 | 1.35% | 3.31% | 5.28% | 3+2 |
| 2018-07-01..2019-01-01 | 2.42% | -0.52% | -3.51% | 2+3 |
| 2019-07-01..2020-01-01 | -3.12% | 0.83% | 4.77% | 3+2 |
| 2020-07-01..2021-01-01 | -3.17% | 3.24% | 9.69% | 4+3 |
| 2021-07-01..2022-01-01 | 0.70% | 3.34% | 5.98% | 3+2 |
| 2022-07-01..2023-01-01 | -1.71% | -0.55% | 0.58% | 2+3 |
| 2023-07-01..2024-01-01 | 2.67% | 3.44% | 4.20% | 3+2 |
| 2024-07-01..2025-01-01 | 3.01% | 3.52% | 4.03% | 2+2 |
| 2025-07-01..2026-01-01 | 3.01% | 4.12% | 5.23% | 2+1 |
| **Compounded** | **2.79%** | 23.39% | 46.79% | |

Long/short ranks above long-only in 1 of 10 windows. Shorting the below-average periods lost money in this sample: SPY kept rising through most of them (2019 H2, 2020 H2), so the short leg paid more in losses than the avoided drawdowns saved. Same caveats as above; the borrow rate is an assumption, not a quote, and dividends owed on shorts are not charged.
