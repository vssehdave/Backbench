# 2.37 Put ratio backspread

- Section: 2.37
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 1 x n put contracts at spot*1.0000; long 2 x n put contracts at spot*0.9750. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This strategy consists of a short position in N S close to ATM put options with a strike price K 1, and a long position in N L OTM put options with a strike price K 2, where N L \> N S. Typically, N L = 2 and N S = 1, or N L = 3 and N S = 2. The trader's outlook is strongly bearish. This is a capital gain strategy. We have:

fT = NL × (K2 −ST)+ −NS × (K1 −ST)+ −H (153) S∗up = K1 + H/NS, H < 0 (154) S∗down = (NL \times K2 −NS \times K1 −H)/(NL −NS) (155) Pmax = NL \times K2 −NS \times K1 −H (156) $$ Lmax = NS \times (K1 −K2) + H $$ (157)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.37. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| put ratio backspread | -1.4% | -15.3% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 14, assignments 9, fees USD 132.60, missing-bar days 3, mark gaps 2. Return at half-spreads 0 / 0.05 / 0.10: -0.9% / -2.0% / -3.0%.
