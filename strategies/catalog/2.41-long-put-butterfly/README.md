# 2.41 Long put butterfly

- Section: 2.41
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n put contracts at spot*0.9750; short 2 x n put contracts at spot*1.0000; long 1 x n put contracts at spot*1.0250. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a sideways strategy consisting of a long position in an OTM put option with a strike price K 1, a short position in two ATM put options with a strike price K 2, and a long position in an ITM put option with a strike price K 3. The strikes are equidistant: K 3 − K 2 = K 2 − K 1 = κ. This is a relatively low cost net debit trade. The trader's outlook is neutral. This is a capital gain strategy. We have:

$$ fT = (K1 −ST)+ + (K3 −ST)+ −2 \times (K2 −ST)+ −D $$ (177) *S ∗ up = K 3 − D (178) S∗down = K1 + D (179) Pmax = \kappa −D (180) *L max = D (181)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.41. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| long put butterfly | 11.1% | -10.8% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 35, assignments 9, fees USD 176.80, missing-bar days 30, mark gaps 51. Return at half-spreads 0 / 0.05 / 0.10: 11.6% / 10.3% / 8.9%.
