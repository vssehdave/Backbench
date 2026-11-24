# 3.13 Three moving averages

- Section: 3.13
- Asset class: Stocks
- Harness status: **tested**. Rule as implemented: Long if MA(3) > MA(10) > MA(21), liquidate if MA(3) <= MA(10), otherwise hold (the paper's example values). Long-only.

## Description (paper)

In some cases, using 3 moving averages with lengths T 1 \< T 2 \< T 3 (e.g., T 1 = 3, *T 2 = 10, T 3 = 21) can help filter false signals: Signal =         

Establish long position if MA(T1) > MA(T2) > MA(T3) Liquidate long position if MA( *T 1 ) ≤ MA( *T 2 ) Establish short position if MA(T1) < MA(T2) < MA(T3) Liquidate short position if MA( *T 1 ) ≥ MA( *T 2 ) (324)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.13. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

Real data: SPY daily raw SIP bars from Alpaca, 2016-01-01 to 2026-01-01 (exclusive), run with `python money.py test 3.13-three-moving-averages/manifest.json --start 2016-01-01 --end 2026-01-01` (saved as `results.json`). Defaults: 20 stress paths, 10 bps shock, seed 42.

| Forward window | Selected | Strategy | Cash | Buy and hold | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 21 | 1.14% | 0.00% | 3.39% | 5+5 |
| 2017-07-01..2018-01-01 | 21 | 3.31% | 0.00% | 5.28% | 5+4 |
| 2018-07-01..2019-01-01 | 21 | -0.34% | 0.00% | -3.51% | 6+6 |
| 2019-07-01..2020-01-01 | 21 | 4.63% | 0.00% | 4.77% | 5+4 |
| 2020-07-01..2021-01-01 | 21 | 3.14% | 0.00% | 9.69% | 7+6 |
| 2021-07-01..2022-01-01 | 21 | 1.35% | 0.00% | 5.98% | 7+6 |
| 2022-07-01..2023-01-01 | 21 | -0.92% | 0.00% | 0.58% | 5+5 |
| 2023-07-01..2024-01-01 | 21 | 4.97% | 0.00% | 4.20% | 4+3 |
| 2024-07-01..2025-01-01 | 21 | -1.14% | 0.00% | 4.03% | 8+8 |
| 2025-07-01..2026-01-01 | 21 | -1.33% | 0.00% | 5.23% | 9+8 |
| **Compounded** | | **15.53%** | 0.00% | 46.79% | |

Strategy ranks above buy and hold in 2 of 10 windows; abstentions 156. Cash and buy-and-hold are the repo's own `controls:cash` and `controls:buy_and_hold` run through the same folds, fees and sizing (`../_benchmarks/`).

Read with care:
- Only the second half of each calendar year (July-December) is a forward window; the other half trains. Ten windows cover half the decade, so the compounded numbers are not a ten-year return.
- Each window is one 6-month sample, and the level is chosen per window on a 3-month selection slice, so the selected level changes.
- Prices are raw (no dividends), which understates buy-and-hold and the long legs equally.
- Signals use the prior close and fill at the next open, with the repo's IBKR fee model; position is a fixed share count of about 5,000 USD at the window's first training close (half of the 10,000 USD of cash).
- Parameters are the paper's examples where it gives them, otherwise the author's fixed choice (see Harness status), and were not changed after seeing results.
