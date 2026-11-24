# 2.50 Long iron condor

- Section: 2.50
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This sideways strategy is a combination of a bull put spread and a bear call spread and consists of a long position in an OTM put option with a strike price K 1, a short position in an OTM put option with a higher strike price K 2, a short position in an OTM call option with a strike price K 3, and a long position in an OTM call option with a higher strike price K 4. The strikes are equidistant: K 4 − K 3 = K 3 − K 2 = *K 2 − K 1 = κ. This is a net credit trade. The trader's outlook is neutral. This is an income strategy. We have:

$$ fT = (K1 −ST)+ + (ST −K4)+ −(K2 −ST)+ −(ST −K3)+ + C $$ (226) S∗up = K3 + C (227) *S ∗ down = K 2 − C (228) *P max = C (229) Lmax = \kappa −C (230)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.50. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
