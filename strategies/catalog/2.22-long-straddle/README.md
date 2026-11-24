# 2.22 Long straddle

- Section: 2.22
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a volatility strategy consisting of a long position in an ATM call option, and a long position in an ATM put option with a strike price K. This is a net debit trade. The trader's outlook is neutral. This is a capital gain strategy. We have 22:

$$ fT = (ST −K)+ + (K −ST)+ −D $$ (81) S∗up = K + D (82) *S ∗ down = K − D (83) *P max = unlimited (84) *L max = D (85)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.22. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
