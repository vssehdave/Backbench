# 2.14 Bull call ladder

- Section: 2.14
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a vertical spread consisting of a long position in (usually) a close to ATM call option with a strike price K 1, a short position in an OTM call option with a strike price K 2, and a short position in another OTM call option with a higher strike price K 3. A bull call ladder is a bull call spread financed by selling another OTM call option (with the strike price K 3 ). 18 This adjusts the trader's outlook from bullish (bull call spread) to conservatively bullish or even non-directional (with an expectation of low volatility). We have:

$$ fT = (ST −K1)+ −(ST −K2)+ −(ST −K3)+ −H $$ (53) S∗down = K1 + H, H > 0 (54) S∗up = K3 + K2 −K1 −H (55) Pmax = K2 −K1 −H (56) *L max = unlimited (57)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.14. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
