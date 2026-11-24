# 2.45 "Short" iron butterfly

- Section: 2.45
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This volatility strategy is a combination of a bear put spread and a bull call spread and consists of a short position in an OTM put option with a strike price K 1, a long position in an ATM put option and an ATM call option with a strike price *K 2, and a short position in an OTM call option with a strike price K 3. The strikes are equidistant: K 2 − K 1 = K 3 − K 2 = κ. This is a net debit trade. The trader's outlook is neutral. This is a capital gain strategy. We have:

$$ fT = (K2 −ST)+ + (ST −K2)+ −(K1 −ST)+ −(ST −K3)+ −D (201) $$ S∗up = K2 + D (202) *S ∗ down = K 2 − D (203) Pmax = \kappa −D (204) *L max = D (205)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.45. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
