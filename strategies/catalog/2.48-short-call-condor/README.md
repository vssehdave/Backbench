# 2.48 Short call condor

- Section: 2.48
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a volatility strategy consisting of a short position in an ITM call option with a strike price K 1, a long position in an ITM call option with a higher strike price K 2, a long position in an OTM call option with a strike price K 3, and a short position in an OTM call option with a higher strike price K 4. All strikes are equidistant: *K 4 − K 3 = K 3 − K 2 = K 2 − K 1 = κ. This is a relatively low net credit trade. As with a short call butterfly, the potential reward is sizably smaller than with a short straddle or a short strangle (albeit with a lower risk). So, this is a capital gain (rather than an income) strategy. The trader's outlook is neutral. We have:

$$ fT = (ST −K2)+ + (ST −K3)+ −(ST −K1)+ −(ST −K4)+ + C $$ (216) *S ∗ up = K 4 − C (217) S∗down = K1 + C (218) *P max = C (219) Lmax = \kappa −C (220)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.48. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
