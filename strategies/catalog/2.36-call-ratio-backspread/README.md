# 2.36 Call ratio backspread

- Section: 2.36
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 1 x n call contracts at spot*1.0000; long 2 x n call contracts at spot*1.0250. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This strategy consists of a short position in N S close to ATM call options with a strike price K 1, and a long position in N L OTM call options with a strike price K 2, where N L \> N S. Typically, N L = 2 and N S = 1, or N L = 3 and N S = 2. The trader's outlook is strongly bullish. This is a capital gain strategy. We have: 27

fT = NL × (ST −K2)+ −NS × (ST −K1)+ −H (148) *S ∗ down = K 1 − H/N S , H < 0 (149) S∗up = (NL \times K2 −NS \times K1 + H)/(NL −NS) (150) *P max = unlimited (151) $$ Lmax = NS \times (K2 −K1) + H $$ (152)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.36. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| call ratio backspread | 9.0% | -7.7% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 38, assignments 25, fees USD 132.60, missing-bar days 21, mark gaps 3. Return at half-spreads 0 / 0.05 / 0.10: 9.4% / 8.4% / 7.4%.
