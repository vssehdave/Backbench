# 2.42 Short call butterfly

- Section: 2.42
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a volatility strategy consisting of a short position in an ITM call option with a strike price K 1, a long position in two ATM call options with a strike price K 2, and a short position in an OTM call option with a strike price K 3. The strikes are equidistant: K 3 − K 2 = K 2 − K 1 = κ. This is a net credit trade. In this sense, this is an income strategy. However, the potential reward is sizably smaller than with a short straddle or a short strangle (albeit with a lower risk). The trader's outlook is neutral. We have:

$$ fT = 2 \times (ST −K2)+ −(ST −K1)+ −(ST −K3)+ + C $$ (186) *S ∗ up = K 3 − C (187) S∗down = K1 + C (188) *P max = C (189) Lmax = \kappa −C (190)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.42. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
