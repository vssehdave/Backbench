# 2.2 Covered call

- Section: 2.2
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy (a.k.a. "buy-write" strategy) amounts to buying stock and writing a call option with a strike price K against the stock position. The trader's outlook on the stock price is neutral to bullish. The covered call strategy has the same payoffas writing a put option (short/naked put). 10 While maintaining the long stock position, the trader can generate income by periodically selling OTM call options. We have: 11

fT = ST −S0 −(ST −K)+ + C = K −S0 −(K −ST)+ + C

(1) S∗= S0 −C (2) Pmax = K −S0 + C (3) *L max = S 0 − C (4)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
