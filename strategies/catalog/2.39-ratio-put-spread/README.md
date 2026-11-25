# 2.39 Ratio put spread

- Section: 2.39
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n put contracts at spot*1.0250; short 2 x n put contracts at spot*1.0000. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This strategy consists of a short position in N S close to ATM put options with a strike price K 1, and a long position in N L ITM put options with a strike price K 2, where N L \< N S. Typically, N L = 1 and N S = 2, or N L = 2 and N S = 3. This is an income strategy if it is structured as a net credit trade. The trader's outlook is neutral to bullish. We have:

fT = NL × (K2 −ST)+ −NS × (K1 −ST)+ −H (163) *S ∗ up = K 2 − H/N L , H > 0 (164) S∗down = (NS \times K1 −NL \times K2 + H)/(NS −NL) (165) Pmax = NL × (K2 −K1) −H (166) Lmax = NS \times K1 −NL \times K2 + H (167)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.39. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| ratio put spread | 22.2% | -14.3% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 30, assignments 9, fees USD 132.60, missing-bar days 29, mark gaps 50. Return at half-spreads 0 / 0.05 / 0.10: 22.6% / 21.6% / 20.5%.
