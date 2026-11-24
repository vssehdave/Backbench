# 2.46 Long call condor

- Section: 2.46
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n call contracts at spot*0.9625; short 1 x n call contracts at spot*0.9875; short 1 x n call contracts at spot*1.0125; long 1 x n call contracts at spot*1.0375. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a sideways strategy consisting of a long position in an ITM call option with a strike price K 1, a short position in an ITM call option with a higher strike price K 2, a short position in an OTM call option with a strike price K 3, and a long position in an OTM call option with a higher strike price K 4. All strikes are equidistant: *K 4 − K 3 = K 3 − K 2 = K 2 − K 1 = κ. This is a relatively low cost net debit trade. The trader's outlook is neutral. This is a capital gain strategy. We have:

fT = (ST −K1)+ −(ST −K2)+ −(ST −K3)+ + (ST −K4)+ −D (206)

*S ∗ up = K 4 − D (207) S∗down = K1 + D (208) Pmax = \kappa −D (209) *L max = D (210)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.46. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| long call condor | 0.1% | -19.0% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 79, assignments 44, fees USD 176.80, missing-bar days 70, mark gaps 143. Return at half-spreads 0 / 0.05 / 0.10: 0.7% / -0.7% / -2.0%.
