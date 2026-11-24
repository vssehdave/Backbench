# 2.40.1 Modified call butterfly

- Section: 2.40.1
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a variation of the long call butterfly strategy where the strikes are no longer equidistant; instead we have K 1 *− K 2 \< K 2 *− K 3. This results in a sideways strategy with a bullish bias. We have:

$$ fT = (ST −K1)+ + (ST −K3)+ −2 \times (ST −K2)+ −D $$ (173) $$ S∗= K3 + D $$ (174) Pmax = K2 −K3 −D (175) *L max = D (176)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.40.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
