# 2.11 Short synthetic forward

- Section: 2.11
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy amounts to buying an ATM put option and selling an ATM call option with a strike price K = S 0. This can be a net debit or net credit trade. Typically, *\| H \| ≪ S 0. The trader's outlook is bearish: this strategy mimics a short stock or futures position; it replicates a short forward contract with the delivery price K and the same maturity as the options. This is a capital gain strategy. We have:

fT = (K −ST)+ −(ST −K)+ −H = K −ST −H (37) *S ∗ = K − H (38) *P max = K − H (39) *L max = unlimited (40)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.11. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
