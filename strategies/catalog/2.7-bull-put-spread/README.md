# 2.7 Bull put spread

- Section: 2.7
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a vertical spread consisting of a long position in an OTM put option with a strike price K 1, and a short position in another OTM put option with a higher strike price K 2. This is a net credit trade. The trader's outlook is bullish. This is an income strategy. We have:

fT = (K1 −ST)+ −(K2 −ST)+ + C

(21) S∗= K2 −C (22) *P max = C (23) Lmax = K2 −K1 −C (24)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.7. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
