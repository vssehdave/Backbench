# 2.35 Strip

- Section: 2.35
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a volatility strategy consisting of a long position in an ATM call option, and a long position in two ATM put options with a strike price K. This is a net debit trade. The trader's outlook is bearish. This is a capital gain strategy. We have:

$$ fT = (ST −K)+ + 2 \times (K −ST)+ −D $$ (143) S∗up = K + D (144) *S ∗ down = K − D (145)

*P max = unlimited (146) *L max = D (147)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.35. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
