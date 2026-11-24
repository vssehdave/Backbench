# 2.33 Covered short strangle

- Section: 2.33
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy amounts to augmenting a covered call by writing an OTM put option with a strike price K ′ and the same TTM as the sold call option (whose strike price is K) and thereby increasing the income. The trader's outlook is bullish. We have:

fT = ST −S0 −(ST −K)+ −(K′ −ST)+ + C

(135) Pmax = K −S0 + C (136) Lmax = S0 + K′ −C (137)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.33. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
