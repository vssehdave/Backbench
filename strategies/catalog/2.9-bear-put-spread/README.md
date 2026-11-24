# 2.9 Bear put spread

- Section: 2.9
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a vertical spread consisting of a long position in a close to ATM put option with a strike price K 1, and a short position in an OTM put option with a lower

strike price K 2. This is a net debit trade. The trader's outlook is bearish: this strategy profits if the stock price falls. This is a capital gain strategy. We have:

fT = (K1 −ST)+ −(K2 −ST)+ −D

(29) S∗= K1 −D (30) Pmax = K1 −K2 −D (31) *L max = D (32)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.9. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
