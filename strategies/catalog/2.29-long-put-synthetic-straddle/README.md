# 2.29 Long put synthetic straddle

- Section: 2.29
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This volatility strategy (which is the same as a long straddle with the call replaced by a synthetic call) amounts to buying stock and buying two ATM (or the nearest ITM) put options with a strike price K. The trader's outlook is neutral. This is a capital gain strategy. We have (assuming S 0 ≤ K and D \> K − S 0 ):

$$ fT = ST −S0 + 2 \times (K −ST)+ −D $$ (116) S∗up = S0 + D (117) S∗down = 2 \times K −S0 −D (118) *P max = unlimited (119) Lmax = D −(K −S0) (120)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.29. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
