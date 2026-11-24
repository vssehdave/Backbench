# 7.6 Volatility trading with variance swaps

- Section: 7.6
- Asset class: Volatility
- Harness status: **not testable: futures** - needs VIX futures or ETN, option or variance-swap data.

## Description (paper)

One issue with trading volatility using options is the need to (almost continuously) Delta-hedge the position to avoid directional exposure, 137 which practically can be both cumbersome and costly. To avoid the need for Delta-hedging, one can make volatility bets using variance swaps. A variance swap is a derivative contract whose payoff *P ( *T) at maturity T is proportional to the difference between the realized variance v ( *T) of the underlying and the preset variance strike K: $$ P(T) = N \times (v(T) −K) $$ (434) $$ v(T) = F $$

T

T X $$ t=1 $$ *R 2 ( *t) (435) $$ R(t) = ln $$  *S ( *t) *S ( *t − 1)  (436)

Here: t = 0 , 1 ,..., T labels sample points (e.g., trading days); S ( *t) is the price of the underlying at time t; R ( *t) is the log-return from t − 1 to t; F is the annualization factor (thus, if t labels trading days, then F = 252); and N is the "variance notional", which is preset. Note that in Eq. (435) the mean of R ( *t) over the period t = 1 to *t = T is not subtracted, hence T in the denominator. 138 Long (short) variance swap

is a bet that the future realized volatility will be higher (lower) than the current implied volatility. Long (short) variance swaps can therefore be used instead of, e.g., long (short) straddles to go long (short) volatility. For instance, the dispersion strategy of Subsection 6.3 can be executed by selling a variance swap on an index and buying variance swaps on the index constituents (cf. selling and buying straddles). 139

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 7.6. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
