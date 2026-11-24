# 7.3.1 Hedging short VXX with VIX futures

- Section: 7.3.1
- Asset class: Volatility
- Harness status: **not testable: futures** - needs VIX futures or ETN, option or variance-swap data.

## Description (paper)

Instead of using a long position in VXZ to hedge the short position in VXX, one can directly use a basket of, e.g., medium-maturity VIX futures. 132 The N VIX futures have some weights w i. These weights can be fixed in a variety of ways, e.g., by minimizing the tracking error, i.e., by running a serial regression (with the intercept) of VXX returns over the N futures returns. Then we have: $$ wi = \sigmaX $$

N X $$ j=1 $$ *− 1 ij \sigmaj\rhoj (432)

131 We have h = β = ρσ X /σ Z, where: h (known as the optimal hedge ratio) is the number of VXZ to buy for each VXX shorted; β is the coefficient (for the VXZ returns) of the serial regression (with the intercept) of the VXX returns over the VXZ returns; σ X and σ Z are the historical volatilities of VXX and VXZ, respectively; and ρ is the pair-wise historical correlation between VXX and VXZ.

Here: ρ i is the pair-wise historical correlation between the futures labeled by i and VXX; C ij is the N × N sample covariance matrix for the N futures ( *σ 2

*i = C ii is the historical variance for the futures labeled by i); and σ X is the historical volatility of VXX. Some w i may turn out to be negative. This is not necessarily an issue, but one may wish to impose the bounds w i ≥ 0. Further, one may wish the strategy to be dollar-neutral, which would amount to imposing the constraint

N X $$ i=1 $$ $$ wi = 1 $$ (433)

which the optimal hedge ratios (432) generally do not satisfy. Also, instead of minimizing the tracking error, one may wish to minimize the variance of the entire portfolio. And so on. The portfolio can be rebalanced monthly or more frequently.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 7.3.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
