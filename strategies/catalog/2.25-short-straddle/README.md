# 2.25 Short straddle

- Section: 2.25
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This a is sideways strategy consisting of a short position in an ATM call option, and a short position in an ATM put option with a strike price K. This is a net credit trade. The trader's outlook is neutral. This is an income strategy. We have:

fT = −(ST −K)+ −(K −ST)+ + C (96) S∗up = K + C (97) *S ∗ down = K − C (98) *P max = C (99) *L max = unlimited (100)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.25. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
