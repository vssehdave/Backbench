# 2.40 Long call butterfly

- Section: 2.40
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a sideways strategy consisting of a long position in an OTM call option with a strike price K 1, a short position in two ATM call options with a strike price K 2, and a long position in an ITM call option with a strike price K 3. The strikes are equidistant: K 2 − K 3 = K 1 − K 2 = κ. This is a relatively low cost net debit trade. The trader's outlook is neutral. This is a capital gain strategy. We have: 29

$$ fT = (ST −K1)+ + (ST −K3)+ −2 \times (ST −K2)+ −D $$ (168) S∗down = K3 + D (169) *S ∗ up = K 1 − D (170) Pmax = \kappa −D (171) *L max = D (172)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.40. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
