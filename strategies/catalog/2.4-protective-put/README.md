# 2.4 Protective put

- Section: 2.4
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy (a.k.a. "married put" or "synthetic call") amounts to buying stock and an ATM or OTM put option with a strike price K ≤ S 0. The trader's outlook is bullish. This is a hedging strategy: the put option hedges the risk of the stock price falling. We have: 13

fT = ST −S0 + (K −ST)+ −D = K −S0 + (ST −K)+ −D (9) $$ S∗= S0 + D $$ (10) *P max = unlimited (11) Lmax = S0 −K + D (12)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.4. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
