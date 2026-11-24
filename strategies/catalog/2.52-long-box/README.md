# 2.52 Long box

- Section: 2.52
- Asset class: Options
- Harness status: **not testable: options chains** - multi-leg option position; needs option chains and prices, while the harness holds shares of one instrument.

## Description (paper)

This volatility strategy can be viewed as a combination of a long synthetic forward and a short synthetic forward, or as a combination of a bull call spread and a bear put spread, and consists of a long position in an ITM put option with a strike price *K 1, a short position in an OTM put option with a lower strike price K 2, a long position in an ITM call option with the strike price K 2, and a short position in an OTM call option with the strike price K 1. The trader's outlook is neutral. This is a capital gain strategy. 31 We have (assuming K 1 ≥ K 2 + D):

T

$$ = $$ ( *K 1 − S T) + − ( *K 2 − S T) + + ( *S T − K 2 ) + − ( *S T − K 1 ) + − D $$ = $$ *K 1 − K 2 − D (236) *max $$ = $$ ( *K 1 − K 2 ) − D (237)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 2.52. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
