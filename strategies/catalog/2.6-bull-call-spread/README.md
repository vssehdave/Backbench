# 2.6 Bull call spread

- Section: 2.6
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a vertical spread consisting of a long position in a close to ATM call option with a strike price K 1, and a short position in an OTM call option with a higher

strike price K 2. This is a net debit trade. The trader's outlook is bullish: the strategy profits if the stock price rises. This is a capital gain strategy. We have: 15

fT = (ST −K1)+ −(ST −K2)+ −D

(17) $$ S∗= K1 + D $$ (18) Pmax = K2 −K1 −D (19) *L max = D (20)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.6. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
