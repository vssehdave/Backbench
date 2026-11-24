# 2.3 Covered put

- Section: 2.3
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy (a.k.a. "sell-write" strategy) amounts to shorting stock and writing a put option with a strike price K against the stock position. The trader's outlook is

neutral to bearish. The covered put strategy has the same payoffas writing a call option (short/naked call). While maintaining the short stock position, the trader can generate income by periodically selling OTM put options. We have: 12

fT = S0 −ST −(K −ST)+ + C = S0 −K −(ST −K)+ + C (5) $$ S∗= S0 + C $$ (6) Pmax = S0 −K + C (7) *L max = unlimited (8)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
