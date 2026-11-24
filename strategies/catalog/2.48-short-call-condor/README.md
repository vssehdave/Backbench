# 2.48 Short call condor

- Section: 2.48
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 1 x n call contracts at spot*0.9625; long 1 x n call contracts at spot*0.9875; long 1 x n call contracts at spot*1.0125; short 1 x n call contracts at spot*1.0375. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a volatility strategy consisting of a short position in an ITM call option with a strike price K 1, a long position in an ITM call option with a higher strike price K 2, a long position in an OTM call option with a strike price K 3, and a short position in an OTM call option with a higher strike price K 4. All strikes are equidistant: *K 4 − K 3 = K 3 − K 2 = K 2 − K 1 = κ. This is a relatively low net credit trade. As with a short call butterfly, the potential reward is sizably smaller than with a short straddle or a short strangle (albeit with a lower risk). So, this is a capital gain (rather than an income) strategy. The trader's outlook is neutral. We have:

$$ fT = (ST −K2)+ + (ST −K3)+ −(ST −K1)+ −(ST −K4)+ + C $$ (216) *S ∗ up = K 4 − C (217) S∗down = K1 + C (218) *P max = C (219) Lmax = \kappa −C (220)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.48. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| short call condor | -1.6% | -17.1% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 79, assignments 35, fees USD 176.80, missing-bar days 70, mark gaps 143. Return at half-spreads 0 / 0.05 / 0.10: -1.0% / -2.4% / -3.7%.
