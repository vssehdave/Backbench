# 2.49 Short put condor

- Section: 2.49
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a volatility strategy consisting of a short position in an OTM put option with a strike price K 1, a long position in an OTM put option with a higher strike price K 2, a long position in an ITM put option with a strike price K 3, and a short position in an ITM put option with a higher strike price K 4. All strikes are equidistant: *K 4 − K 3 = K 3 − K 2 = K 2 − K 1 = κ. This is a relatively low net credit trade.

As with a short put butterfly, the potential reward is sizably smaller than with a short straddle or a short strangle (albeit with a lower risk). So, this is a capital gain (rather than an income) strategy. The trader's outlook is neutral. We have:

$$ fT = (K2 −ST)+ + (K3 −ST)+ −(K1 −ST)+ −(K4 −ST)+ + C $$ (221) *S ∗ up = K 4 − C (222) S∗down = K1 + C (223) *P max = C (224) Lmax = \kappa −C (225)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.49. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
