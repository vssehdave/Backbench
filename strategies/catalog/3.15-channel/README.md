# 3.15 Channel

- Section: 3.15
- Asset class: Stocks
- Harness status: **tested**. Rule as implemented: Donchian channel on closes (the paper's eq. 329-330 use closes): buy when the close reaches the T-day floor, liquidate at the ceiling, else hold. T in {10, 30} is the author's choice. Long-only; the paper also shorts at the ceiling.

## Description (paper)

This strategy amounts to buying and selling a stock when it reaches the floor and the ceiling of a channel, respectively. A channel is a range/band, bounded by a ceiling and a floor, within which the stock price fluctuates. The trader's expectation may be that if the floor or the ceiling is reached, the stock price will bounce in the opposite direction. On the other hand, if the stock price breaks through the ceiling or the floor, the trader may conclude that a new trend has emerged and follow this new trend instead. A simple and common definition of a channel is the Donchian Channel \[Donchian, 1960\], where the ceiling B up and the floor B down are defined as follows (with the same notations as above): 57

$$ Bup = max(P(1), P(2),..., P(T)) $$ (329) Bdown = min(P(1), P(2),..., P(T)) (330) A simple trading strategy then is as follows: Signal = (

Establish long/liquidate short position if P = B down Establish short/liquidate long position if P = B up (331)

The wider the channel, the higher the volatility. Usually, the channel indicator is used together with other indicators. E.g., the signal can be more robust when a price reversal (or a channel break) occurs with an increase in the traded volume.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.15. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

Real data: SPY daily raw SIP bars from Alpaca, 2016-01-01 to 2026-01-01 (exclusive), run with `python money.py test 3.15-channel/manifest.json --start 2016-01-01 --end 2026-01-01` (saved as `results.json`). Defaults: 20 stress paths, 10 bps shock, seed 42.

| Forward window | Selected | Strategy | Cash | Buy and hold | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 30 | 0.87% | 0.00% | 3.39% | 1+1 |
| 2017-07-01..2018-01-01 | 10 | 2.14% | 0.00% | 5.28% | 4+4 |
| 2018-07-01..2019-01-01 | 30 | -6.63% | 0.00% | -3.51% | 1+0 |
| 2019-07-01..2020-01-01 | 30 | 2.99% | 0.00% | 4.77% | 1+1 |
| 2020-07-01..2021-01-01 | 30 | 4.15% | 0.00% | 9.69% | 1+1 |
| 2021-07-01..2022-01-01 | 10 | 4.20% | 0.00% | 5.98% | 4+4 |
| 2022-07-01..2023-01-01 | 30 | -0.15% | 0.00% | 0.58% | 2+1 |
| 2023-07-01..2024-01-01 | 30 | 0.52% | 0.00% | 4.20% | 1+1 |
| 2024-07-01..2025-01-01 | 30 | 4.86% | 0.00% | 4.03% | 1+1 |
| 2025-07-01..2026-01-01 | 30 | 2.39% | 0.00% | 5.23% | 1+1 |
| **Compounded** | | **15.87%** | 0.00% | 46.79% | |

Strategy ranks above buy and hold in 1 of 10 windows; abstentions 905. Cash and buy-and-hold are the repo's own `controls:cash` and `controls:buy_and_hold` run through the same folds, fees and sizing (`../_benchmarks/`).

Read with care:
- Only the second half of each calendar year (July-December) is a forward window; the other half trains. Ten windows cover half the decade, so the compounded numbers are not a ten-year return.
- Each window is one 6-month sample, and the level is chosen per window on a 3-month selection slice, so the selected level changes.
- Prices are raw (no dividends), which understates buy-and-hold and the long legs equally.
- Signals use the prior close and fill at the next open, with the repo's IBKR fee model; position is a fixed share count of about 5,000 USD at the window's first training close (half of the 10,000 USD of cash).
- Parameters are the paper's examples where it gives them, otherwise the author's fixed choice (see Harness status), and were not changed after seeing results.
