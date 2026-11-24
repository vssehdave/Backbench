# 2.41.1 Modified put butterfly

- Section: 2.41.1
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a variation of the long put butterfly strategy where the strikes are no longer equidistant; instead we have K 3 *− K 2 \< K 2 *− K 1. This results in a sideways strategy with a bullish bias. We have (for H \> 0 there is also S ∗ up = K 3 − H): 30

$$ fT = (K1 −ST)+ + (K3 −ST)+ −2 \times (K2 −ST)+ −H $$ (182) S∗down = 2 \times K2 −K3 + H (183) Pmax = K3 −K2 −H (184) $$ Lmax = 2 \times K2 −K1 −K3 + H $$ (185)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.41.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
