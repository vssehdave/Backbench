# 2.44 "Long" iron butterfly

- Section: 2.44
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This sideways strategy is a combination of a bull put spread and a bear call spread and consists of a long position in an OTM put option with a strike price K 1, a short position in an ATM put option and an ATM call option with a strike price *K 2, and a long position in an OTM call option with a strike price K 3. The strikes are equidistant: K 2 − K 1 = K 3 − K 2 = κ. This is a net credit trade. The trader's outlook is neutral. This is an income strategy. We have:

$$ fT = (K1 −ST)+ −(K2 −ST)+ −(ST −K2)+ + (ST −K3)+ + C $$ (196) S∗up = K2 + C (197) *S ∗ down = K 2 − C (198) *P max = C (199) Lmax = \kappa −C (200)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.44. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
