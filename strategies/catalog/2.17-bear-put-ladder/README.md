# 2.17 Bear put ladder

- Section: 2.17
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This is a vertical spread consisting of a long position in (usually) a close to ATM put option with a strike price K 1, a short position in an OTM put option with a strike price K 2, and a short position in another OTM put option with a lower strike price K 3. A bear put ladder is a bear put spread financed by selling another OTM put option (with the strike price K 3 ). 20 This adjusts the trader's outlook from bearish (bear put spread) to conservatively bearish or even non-directional (with an

expectation of low volatility). We have (assuming K 3 + K 2 − K 1 + H \> max( *H, 0)):

$$ fT = (K1 −ST)+ −(K2 −ST)+ −(K3 −ST)+ −H $$ (68) *S ∗ up = K 1 − H, H > 0 (69) S∗down = K3 + K2 −K1 + H (70) Pmax = K1 −K2 −H (71) $$ Lmax = K3 + K2 −K1 + H $$ (72)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.17. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
