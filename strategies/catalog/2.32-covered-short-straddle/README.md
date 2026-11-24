# 2.32 Covered short straddle

- Section: 2.32
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy amounts to augmenting a covered call by writing a put option with the same strike price K and TTM as the sold call option and thereby increasing the income. The trader's outlook is bullish. We have:

fT = ST −S0 −(ST −K)+ −(K −ST)+ + C (131)

S∗= 1

2 ( S 0 + K − C ) (132) Pmax = K −S0 + C (133) Lmax = S0 + K −C (134)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.32. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
