# 2.34 Strap

- Section: 2.34
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a volatility strategy consisting of a long position in two ATM call options, and a long position in an ATM put option with a strike price K. This is a net debit trade. The trader's outlook is bullish. This is a capital gain strategy. We have: 26

$$ fT = 2 \times (ST −K)+ + (K −ST)+ −D $$ (138) S∗up = K + D (139)

*S ∗ down = K − D (140) *P max = unlimited (141) *L max = D (142)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.34. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
