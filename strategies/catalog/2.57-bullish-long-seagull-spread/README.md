# 2.57 Bullish long seagull spread

- Section: 2.57
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This option trading strategy is a long combo (long risk reversal) hedged against the stock price falling by buying an OTM put option. It amounts to a long position in an OTM put option with a strike price K 1, a short position in an ATM put option with a strike price K 2, and a long position in an OTM call option with a strike price *K 3. Ideally, the trade should be structured to have zero cost. The trader's outlook is bullish. This is a capital gain strategy. We have:

$$ fT = (K1 −ST)+ −(K2 −ST)+ + (ST −K3)+ −H $$ (260) S∗= K3 + H, H > 0 (261) S∗= K2 + H, H < 0 (262) $$ K2 \leqS∗\leqK3, $$ $$ H = 0 $$ (263) *P max = unlimited (264) Lmax = K2 −K1 + H (265)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.57. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
