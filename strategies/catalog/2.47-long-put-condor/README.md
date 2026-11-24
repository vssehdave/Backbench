# 2.47 Long put condor

- Section: 2.47
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: long 1 x n put contracts at spot*0.9625; short 1 x n put contracts at spot*0.9875; short 1 x n put contracts at spot*1.0125; long 1 x n put contracts at spot*1.0375. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a sideways strategy consisting of a long position in an OTM put option with a strike price K 1, a short position in an OTM put option with a higher strike price K 2, a short position in an ITM put option with a strike price K 3, and a long position in an ITM put option with a higher strike price K 4. All strikes are equidistant: *K 4 − K 3 = K 3 − K 2 = K 2 − K 1 = κ. This is a relatively low cost net debit trade. The trader's outlook is neutral. This is a capital gain strategy. We have:

$$ fT = (K1 −ST)+ −(K2 −ST)+ −(K3 −ST)+ + (K4 −ST)+ −D (211) $$ *S ∗ up = K 4 − D (212) S∗down = K1 + D (213) Pmax = \kappa −D (214) *L max = D (215)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.47. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| long put condor | 12.4% | -9.6% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 57, assignments 24, fees USD 176.80, missing-bar days 81, mark gaps 139. Return at half-spreads 0 / 0.05 / 0.10: 13.0% / 11.6% / 10.2%.
