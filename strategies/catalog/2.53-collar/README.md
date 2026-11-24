# 2.53 Collar

- Section: 2.53
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy (a.k.a. "fence") is a covered call augmented by a long put option as insurance against the stock price falling. 32 It amounts to buying stock, buying an OTM put option with a strike price K 1, and selling an OTM call option with a higher strike price K 2. The trader's outlook is moderately bullish. This is a capital gain strategy. We have: 33

fT = ST −S0 + (K1 −ST)+ −(ST −K2)+ −H

(238) $$ S∗= S0 + H $$ (239) Pmax = K2 −S0 −H (240) Lmax = S0 −K1 + H (241)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.53. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
