# 2.12 Long combo

- Section: 2.12
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy (a.k.a. "long risk reversal") amounts to buying an OTM call option with a strike price K 1 and selling an OTM put option with a strike price K 2. The

trader's outlook is bullish. This is a capital gain strategy. 17 We have ( *K 1 \> K 2 ):

$$ fT = (ST −K1)+ −(K2 −ST)+ −H $$ (41) S∗= K1 + H, H > 0 (42) S∗= K2 + H, H < 0 (43) $$ K2 \leqS∗\leqK1, $$ $$ H = 0 $$ (44) *P max = unlimited (45) Lmax = K2 + H (46)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.12. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
