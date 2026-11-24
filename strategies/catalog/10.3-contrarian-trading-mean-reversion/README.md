# 10.3 Contrarian trading (mean-reversion)

- Section: 10.3
- Asset class: Futures
- Harness status: **not testable: futures** - needs futures data and positions.

## Description (paper)

This strategy is similar to the mean-reversion strategy discussed in Subsection 3.9. Within a given universe of futures labeled by i = 1 ,..., N, the "market index" return is calculated as an equally weighted average: $$ Rm = 1 $$

N

N X $$ i=1 $$

where R i are the individual futures returns (typically over the last one week). The capital allocation weights w i then are given by wi = −\gamma [Ri −Rm] (470)

where γ \> 0 is fixed via the normalization condition

N X $$ i=1 $$ |wi| = 1 (471)

Note that the strategy is automatically dollar-neutral. It amounts to buying losers and selling winners w.r.t. the market index (see, e.g., \[Wang and Yu, 2004\]). 168 As in the case of equities, the simple weighting scheme given by Eq. (470) is prone to overinvesting in volatile futures, which can be mitigated by suppressing w i by 1 */σ i or 1/\sigma2

*i, where σ i are the historical volatilities. The portfolio is rebalanced weekly.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 10.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
