# 2.5 Protective call

- Section: 2.5
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy (a.k.a. "married call" or "synthetic put") amounts to shorting stock and buying an ATM or OTM call option with a strike price K ≥ S 0. The trader's outlook is bearish. This is a hedging strategy: the call option hedges the risk of the stock price rising. We have: 14

fT = S0 −ST + (ST −K)+ −D = S0 −K + (K −ST)+ −D

(13) S∗= S0 −D (14) *P max = S 0 − D (15) Lmax = K −S0 + D (16)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.5. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
