# 3.11 Single moving average

- Section: 3.11
- Asset class: Stocks
- Harness status: **tested**. Rule as implemented: Long when the close is above its T-day simple moving average, flat when below (long-only; the paper also allows shorting). T in {10, 30} is the author's choice, the paper gives no value.

## Description (paper)

This strategy is based on the stock price crossing a moving average. One can use different types of moving averages (MAs), such as a simple moving average (SMA),

SMA(T) = 1

T

T X $$ t=1 $$ *P ( *t) (319) $$ EMA(T, \lambda) = $$

T $$ t=1 \lambdat−1 P(t) $$ *T $$ t=1 \lambdat−1 $$ $$ = 1 −\lambda $$ 1 −\lambdaT

T X $$ t=1 $$ \lambdat−1 P(t) (320)

Here: t = 1 corresponds to the most recent time in the time series of historical stock prices P ( *t); T is the length of the MA ( *t and T are usually measured in trading days); and λ \< 1 is the factor which suppresses past contributions. Below MA will refer to SMA or EMA. A simple strategy is defined as follows ( *P is the price at *t = 0, on the trading day immediately following the most recent trading day t = 1 in the time series P ( *t)): Signal = (

Establish long/liquidate short position if P \> MA( *T) Establish short/liquidate long position if P \< MA( *T) (321)

This strategy can be run as, e.g., long-only, short-only, or both long and short. It can be straightforwardly applied to multiple stocks (on a single-stock basis, with no cross-sectional interaction between the signals for individual stocks). With a large number of stocks, it may be possible to construct (near-)dollar-neutral portfolios.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.11. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

Real data: SPY daily raw SIP bars from Alpaca, 2016-01-01 to 2026-01-01 (exclusive), run with `python money.py test 3.11-single-moving-average/manifest.json --start 2016-01-01 --end 2026-01-01` (saved as `results.json`). Defaults: 20 stress paths, 10 bps shock, seed 42.

| Forward window | Selected | Strategy | Cash | Buy and hold | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 30 | 0.99% | 0.00% | 3.39% | 8+7 |
| 2017-07-01..2018-01-01 | 10 | 3.54% | 0.00% | 5.28% | 11+10 |
| 2018-07-01..2019-01-01 | 10 | 1.26% | 0.00% | -3.51% | 8+8 |
| 2019-07-01..2020-01-01 | 30 | 2.84% | 0.00% | 4.77% | 5+4 |
| 2020-07-01..2021-01-01 | 30 | 3.86% | 0.00% | 9.69% | 6+5 |
| 2021-07-01..2022-01-01 | 10 | 0.26% | 0.00% | 5.98% | 11+10 |
| 2022-07-01..2023-01-01 | 30 | 1.86% | 0.00% | 0.58% | 2+2 |
| 2023-07-01..2024-01-01 | 30 | 4.55% | 0.00% | 4.20% | 6+5 |
| 2024-07-01..2025-01-01 | 30 | -1.60% | 0.00% | 4.03% | 6+6 |
| 2025-07-01..2026-01-01 | 30 | 2.41% | 0.00% | 5.23% | 7+6 |
| **Compounded** | | **21.70%** | 0.00% | 46.79% | |

Strategy ranks above buy and hold in 3 of 10 windows; abstentions 0. Cash and buy-and-hold are the repo's own `controls:cash` and `controls:buy_and_hold` run through the same folds, fees and sizing (`../_benchmarks/`).

Read with care:
- Only the second half of each calendar year (July-December) is a forward window; the other half trains. Ten windows cover half the decade, so the compounded numbers are not a ten-year return.
- Each window is one 6-month sample, and the level is chosen per window on a 3-month selection slice, so the selected level changes.
- Prices are raw (no dividends), which understates buy-and-hold and the long legs equally.
- Signals use the prior close and fill at the next open, with the repo's IBKR fee model; position is a fixed share count of about 5,000 USD at the window's first training close (half of the 10,000 USD of cash).
- Parameters are the paper's examples where it gives them, otherwise the author's fixed choice (see Harness status), and were not changed after seeing results.
