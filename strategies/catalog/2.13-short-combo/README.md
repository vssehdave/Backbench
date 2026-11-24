# 2.13 Short combo

- Section: 2.13
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This strategy (a.k.a. "short risk reversal") amounts to buying an OTM put option with a strike price K 1 and selling an OTM call option with a strike price K 2. The trader's outlook is bearish. This is a capital gain strategy. We have ( *K 2 \> K 1 ):

$$ fT = (K1 −ST)+ −(ST −K2)+ −H $$ (47) S∗= K1 −H, H > 0 (48) S∗= K2 −H, H < 0 (49) $$ K1 \leqS∗\leqK2, $$ $$ H = 0 $$ (50) *P max = K 1 − H (51) *L max = unlimited (52)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.13. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
