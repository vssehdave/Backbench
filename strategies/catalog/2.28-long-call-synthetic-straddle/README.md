# 2.28 Long call synthetic straddle

- Section: 2.28
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This volatility strategy (which is the same as a long straddle with the put replaced by a synthetic put) amounts to shorting stock and buying two ATM (or the nearest ITM) call options with a strike price K. The trader's outlook is neutral. This is a capital gain strategy. 25 We have (assuming S 0 ≥ K and D \> S 0 − K):

$$ fT = S0 −ST + 2 \times (ST −K)+ −D $$ (111) S∗up = 2 \times K −S0 + D (112) *S ∗ down = S 0 − D (113) *P max = unlimited (114) Lmax = D −(S0 −K) (115)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.28. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
