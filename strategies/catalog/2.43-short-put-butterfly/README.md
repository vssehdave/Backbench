# 2.43 Short put butterfly

- Section: 2.43
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a volatility strategy consisting of a short position in an ITM put option with a strike price K 1, a long position in two ATM put options with a strike price K 2, and a short position in an OTM put option with a strike price K 3. The strikes are equidistant: K 2 − K 3 = K 1 − K 2 = κ. This is a net credit trade. In this sense, this is an income strategy. However, the potential reward is sizably smaller than with a short straddle or a short strangle (albeit with a lower risk). The trader's outlook is neutral. We have:

$$ fT = 2 \times (K2 −ST)+ −(K1 −ST)+ −(K3 −ST)+ + C $$ (191) S∗down = K3 + C (192) *S ∗ up = K 1 − C (193) *P max = C (194) Lmax = \kappa −C (195)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.43. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
