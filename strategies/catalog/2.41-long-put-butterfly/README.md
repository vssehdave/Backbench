# 2.41 Long put butterfly

- Section: 2.41
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a sideways strategy consisting of a long position in an OTM put option with a strike price K 1, a short position in two ATM put options with a strike price K 2, and a long position in an ITM put option with a strike price K 3. The strikes are equidistant: K 3 − K 2 = K 2 − K 1 = κ. This is a relatively low cost net debit trade. The trader's outlook is neutral. This is a capital gain strategy. We have:

$$ fT = (K1 −ST)+ + (K3 −ST)+ −2 \times (K2 −ST)+ −D $$ (177) *S ∗ up = K 3 − D (178) S∗down = K1 + D (179) Pmax = \kappa −D (180) *L max = D (181)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.41. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
