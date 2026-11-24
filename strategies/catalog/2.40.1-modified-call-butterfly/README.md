# 2.40.1 Modified call butterfly

- Section: 2.40.1
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n call contracts at spot*0.9500; short 2 x n call contracts at spot*1.0000; long 1 x n call contracts at spot*1.0250. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a variation of the long call butterfly strategy where the strikes are no longer equidistant; instead we have K 1 *− K 2 \< K 2 *− K 3. This results in a sideways strategy with a bullish bias. We have:

$$ fT = (ST −K1)+ + (ST −K3)+ −2 \times (ST −K2)+ −D $$ (173) $$ S∗= K3 + D $$ (174) Pmax = K2 −K3 −D (175) *L max = D (176)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.40.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| modified call butterfly | 13.1% | -11.8% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 68, assignments 25, fees USD 176.80, missing-bar days 47, mark gaps 179. Return at half-spreads 0 / 0.05 / 0.10: 13.6% / 12.2% / 10.9%.
