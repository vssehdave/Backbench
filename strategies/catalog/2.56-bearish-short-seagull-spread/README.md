# 2.56 Bearish short seagull spread

- Section: 2.56
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This option trading strategy is a bear put spread financed with a sale of an OTM call option. It amounts to a short position in an OTM put option with a strike price K 1, a long position in an ATM put option with a strike price K 2, and a short position in an OTM call option with a strike price K 3. Ideally, the trade should be structured to have zero cost. The trader's outlook is bearish. This is a capital gain strategy. We have:

$$ fT = −(K1 −ST)+ + (K2 −ST)+ −(ST −K3)+ −H $$ (254) S∗= K2 −H, H > 0 (255) S∗= K3 −H, H < 0 (256) $$ K2 \leqS∗\leqK3, $$ $$ H = 0 $$ (257) Pmax = K2 −K1 −H (258) *L max = unlimited (259)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.56. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
