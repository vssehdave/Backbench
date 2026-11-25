# 2.40 Long call butterfly

- Section: 2.40
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n call contracts at spot*0.9750; short 2 x n call contracts at spot*1.0000; long 1 x n call contracts at spot*1.0250. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a sideways strategy consisting of a long position in an OTM call option with a strike price K 1, a short position in two ATM call options with a strike price K 2, and a long position in an ITM call option with a strike price K 3. The strikes are equidistant: K 2 − K 3 = K 1 − K 2 = κ. This is a relatively low cost net debit trade. The trader's outlook is neutral. This is a capital gain strategy. We have: 29

$$ fT = (ST −K1)+ + (ST −K3)+ −2 \times (ST −K2)+ −D $$ (168) S∗down = K3 + D (169) *S ∗ up = K 1 − D (170) Pmax = \kappa −D (171) *L max = D (172)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.40. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| long call butterfly | 11.6% | -7.4% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 67, assignments 25, fees USD 176.80, missing-bar days 27, mark gaps 56. Return at half-spreads 0 / 0.05 / 0.10: 12.1% / 10.8% / 9.4%.
