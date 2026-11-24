# 2.55 Bearish long seagull spread

- Section: 2.55
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This option trading strategy is a short combo (short risk reversal) hedged against the stock price rising by buying an OTM call option. It amounts to a long position in an OTM put option with a strike price K 1, a short position in an ATM call option with a strike price K 2, and a long position in an OTM call option with a strike price *K 3. Ideally, the trade should be structured to have zero cost. The trader's outlook is bearish. This is a capital gain strategy. We have:

$$ fT = (K1 −ST)+ −(ST −K2)+ + (ST −K3)+ −H $$ (248) S∗= K1 −H, H > 0 (249) S∗= K2 −H, H < 0 (250) $$ K1 \leqS∗\leqK2, $$ $$ H = 0 $$ (251) *P max = K 1 − H (252) Lmax = K3 −K2 + H (253)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.55. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
