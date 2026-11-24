# 2.50 Long iron condor

- Section: 2.50
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n put contracts at spot*0.9625; short 1 x n put contracts at spot*0.9875; short 1 x n call contracts at spot*1.0125; long 1 x n call contracts at spot*1.0375. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This sideways strategy is a combination of a bull put spread and a bear call spread and consists of a long position in an OTM put option with a strike price K 1, a short position in an OTM put option with a higher strike price K 2, a short position in an OTM call option with a strike price K 3, and a long position in an OTM call option with a higher strike price K 4. The strikes are equidistant: K 4 − K 3 = K 3 − K 2 = *K 2 − K 1 = κ. This is a net credit trade. The trader's outlook is neutral. This is an income strategy. We have:

$$ fT = (K1 −ST)+ + (ST −K4)+ −(K2 −ST)+ −(ST −K3)+ + C $$ (226) S∗up = K3 + C (227) *S ∗ down = K 2 − C (228) *P max = C (229) Lmax = \kappa −C (230)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.50. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| long iron condor | 8.2% | -4.9% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 29, assignments 20, fees USD 176.80, missing-bar days 50, mark gaps 6. Return at half-spreads 0 / 0.05 / 0.10: 8.8% / 7.4% / 6.0%.
