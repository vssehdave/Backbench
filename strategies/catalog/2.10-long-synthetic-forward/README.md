# 2.10 Long synthetic forward

- Section: 2.10
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy amounts to buying an ATM call option and selling an ATM put option with a strike price K = S 0. This can be a net debit or net credit trade. Typically, *\| H \| ≪ S 0. The trader's outlook is bullish: this strategy mimics a long stock or futures position; it replicates a long forward contract with the delivery price K and the same maturity as the options. This is a capital gain strategy. We have: 16

fT = (ST −K)+ −(K −ST)+ −H = ST −K −H (33) S∗= K + H (34) *P max = unlimited (35) Lmax = K + H (36)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.10. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
