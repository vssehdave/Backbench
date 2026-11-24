# 2.54 Bullish short seagull spread

- Section: 2.54
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This option trading strategy is a bull call spread financed with a sale of an OTM put option. It amounts to a short position in an OTM put option with a strike price K 1, a long position in an ATM call option with a strike price K 2, and a short position in an OTM call option with a strike price K 3. Ideally, the trade should be structured to have zero cost. The trader's outlook is bullish. This is a capital gain

$$ fT = −(K1 −ST)+ + (ST −K2)+ −(ST −K3)+ −H $$ (242) S∗= K2 + H, H > 0 (243) S∗= K1 + H, H < 0 (244) $$ K1 \leqS∗\leqK2, $$ $$ H = 0 $$ (245) Pmax = K3 −K2 −H (246) Lmax = K1 + H (247)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.54. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
