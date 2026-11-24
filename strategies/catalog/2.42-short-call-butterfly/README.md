# 2.42 Short call butterfly

- Section: 2.42
- Asset class: Options
- Harness status: **tested** (own runner `options_bt.py`, not the share harness). Rule as implemented: Each month from one monthly expiry to the next, held to expiry: short 1 x n call contracts at spot*0.9750; long 2 x n call contracts at spot*1.0000; short 1 x n call contracts at spot*1.0250. Low confidence: about 2.8 years of data (2024-01-19 to 2026-11-20), option trade closes rather than quotes, half-spread 0.02 USD/share is an assumption. See `options_manifest.json`, `options_results.json` and docs/options.md.

## Description (paper)

This is a volatility strategy consisting of a short position in an ITM call option with a strike price K 1, a long position in two ATM call options with a strike price K 2, and a short position in an OTM call option with a strike price K 3. The strikes are equidistant: K 3 − K 2 = K 2 − K 1 = κ. This is a net credit trade. In this sense, this is an income strategy. However, the potential reward is sizably smaller than with a short straddle or a short strangle (albeit with a lower risk). The trader's outlook is neutral. We have:

$$ fT = 2 \times (ST −K2)+ −(ST −K1)+ −(ST −K3)+ + C $$ (186) *S ∗ up = K 3 − C (187) S∗down = K1 + C (188) *P max = C (189) Lmax = \kappa −C (190)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.42. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results

SPY 2024-01-19 to 2026-11-20, 34 monthly cycles, USD 100,000 start, price return only. Strikes are fixed offsets from spot (the paper gives none), not tuned.

| | Total return | Max drawdown |
|---|---|---|
| short call butterfly | -13.0% | -18.6% |
| SPY buy and hold | 41.5% | -18.5% |

Opened 34/34 cycles, ITM leg expiries 67, assignments 42, fees USD 176.80, missing-bar days 27, mark gaps 56. Return at half-spreads 0 / 0.05 / 0.10: -12.5% / -13.9% / -15.2%.
