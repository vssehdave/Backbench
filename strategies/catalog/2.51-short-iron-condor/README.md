# 2.51 Short iron condor

- Section: 2.51
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This volatility strategy is a combination of a bear put spread and a bull call spread and consists of a short position in an OTM put option with a strike price K 1, a long position in an OTM put option with a higher strike price K 2, a long position in an OTM call option with a strike price K 3, and a short position in an OTM call option with a higher strike price K 4. The strikes are equidistant: K 4 − K 3 = K 3 − K 2 = *K 2 − K 1 = κ. This is a net debit trade. The trader's outlook is neutral. This is a capital gain strategy. We have:

$$ fT = (K2 −ST)+ + (ST −K3)+ −(K1 −ST)+ −(ST −K4)+ −D (231) $$ S∗up = K3 + D (232) *S ∗ down = K 2 − D (233) Pmax = \kappa −D (234) *L max = D (235)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.51. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
