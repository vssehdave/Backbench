# 10.4 Trend following (momentum)

- Section: 10.4
- Asset class: Futures
- Harness status: **not testable: futures** - needs futures data and positions.

## Description (paper)

Various momentum strategies for futures can be constructed similarly to those for stocks. Here is a simple example (see, e.g., \[Balta and Kosowski, 2013\], \[Moskowitz, Ooi and Pedersen, 2012\]). 170 Let R i be the returns for the futures labeled by i = 1 ,..., N over the past period T (which can be measured in, e.g., days, weeks, or months). Then the weights w i of the trading portfolio are given by $$ wi = \gamma \etai $$ *i (474)

where σ i are the historical volatilities (computed over the period T or some other period), and γ \> 0 is fixed via the normalization condition

N X $$ i=1 $$ |wi| = 1 (476)

Note that this strategy is equivalent to the optimization strategy (see Subsection 3.18, Eq. (350)) with a diagonal covariance matrix C ij = σ 2 *i δ ij (i.e., the correlations between different futures are ignored) and the expected returns E i = η i σ i. This is to be contrasted with the expected returns based on the cumulative returns (Eq. (267)), which in this case equal R i. One issue with using E i = η i σ i as opposed to *E i = R i is that, for small \| R i \| (e.g., compared with σ i), η i can flip even though the change in R i is small. This results in an undesirable instability in the strategy. There are ways to mitigate this, e.g., by smoothing via η i = tanh( *R i /κ), where κ is some parameter, e.g., the cross-sectional standard deviation of R i (see, e.g., \[Kakushadze, 2015b\]). Alternatively, one may simply take E i = R i (and further use a non-diagonal *C ij). Also, note that the weights defined by Eq. (474) are not dollar-neutral. This can be rectified by demeaning them: $$ wi = \gamma $$ " *i i − 1

N

N X $$ j=1 $$ *j j*

(477)

One shortcoming of this is that now some futures with η i \> 0 may be sold, and some futures with η i \< 0 may be bought. To avoid this, if the number N + = \| H + *\| of the

\[DeBondt and Thaler, 1985\], \[Gervais and Odean, 2001\], \[Odean, 2002\], \[Statman, Thorley and Vorkink, 2006\]), so a greater "snap-back" (i.e., mean-reversion) effect can be expected; and ii) open interest is related to trading by hedgers and is a proxy for market depth (see, e.g., \[Bessembinder and Seguin, 1993\]), so an increase in open interest is indicative of a deeper market where volume increases have smaller effects on prices as compared with when there is a decrease in open interest.

futures with η i \> 0 is not dramatically different from the number N − = \| H − \| of the futures with η i \< 0 (here H ± = \{ i \| ± η i \> 0 *\}), we can take the weights to be $$ wi = \gamma+ $$ *i i , i ∈ H + (478) $$ wi = \gamma− $$ *i i , i ∈ H − (479)

So, now we have two parameters γ ±, which can be fixed to satisfy Eq. (476) and the dollar-neutrality condition

N X $$ i=1 $$ $$ wi = 0 $$ (480)

However, if most η i are positive (negative), i.e., we have skewed returns, then long (short) positions will be well-diversified, while the short (long) positions will not be. This can happen, e.g., if the broad market is rallying (selling off). Eq. (477) mitigates this to some extent. However, η i can still be skewed in this case. A simple way to avoid this altogether is to use the demeaned returns e *R i instead of R i, where

e *R i = R i − R m, and the "market index" return R m is defined by Eq. (469). 171 Then *η i = sign( e *R i) are no longer skewed and dollar-neutrality can be achieved as above. 172

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 10.4. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
