# 2.8 Bear call spread

- Section: 2.8
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a vertical spread consisting of a long position in an OTM call option with a strike price K 1, and a short position in another OTM call option with a lower strike price K 2. This is a net credit trade. The trader's outlook is bearish. This is an income strategy. We have:

fT = (ST −K1)+ −(ST −K2)+ + C

(25) $$ S∗= K2 + C $$ (26) *P max = C (27) Lmax = K1 −K2 −C (28)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.8. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
