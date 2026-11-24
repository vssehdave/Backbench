# 3.1 Price-momentum

- Section: 3.1
- Asset class: Stocks
- Harness status: **not testable: cross-sectional universe** - ranks a stock universe by cumulative return, and is long/short (dollar-neutral), which needs short selling.

## Description (paper)

Empirically, there appears to be certain "inertia" in stock returns known as the momentum effect, whereby future returns are positively correlated with past returns (see, e.g., \[Asness, 1994\], \[Asness et al, 2014\], \[Asness, Moskowitz and Pedersen, 2013\], \[Grinblatt and Moskowitz, 2004\], \[Jegadeesh and Titman, 1993\]). Let t denote time measured in the units of 1 month, with t = 0 corresponding to the most recent time. Let P i ( *t) be the time series of prices (fully adjusted for splits and dividends) for the stock labeled by i ( *i = 1 ,..., N, where N is the number of stocks in the trading universe). Let

$$ Ri(t) = $$ *P i ( *t) *P i ( *t + 1) − 1 (266) *cum*

*i $$ = $$ *P i ( *S) *P i ( *S + T) − 1 (267) *mean i $$ = 1 $$

T

S + T − 1 X t=S *R i ( *t) (268) *risk.adj i = R mean i i (269) $$ i = $$ *T − 1

S + T − 1 X t=S ( *R i ( *t) − R mean i) 2 (270)

Here: R i ( *t) is the monthly return; R cum*

*i is the cumulative return computed over the *T -month "formation period" (usually T = 12) skipping the most recent S -month "skip period" (usually S = 1); 35 R mean*

*i is the risk-adjusted mean return over the formation period; and σ i is the monthly volatility calculated over the formation period.

The price-momentum strategy amounts to buying the best performing stocks and selling the worst performing stocks, where the "performance" is measured by a selection criterion based on R cum i, R mean i, R risk.adj*

*i (in the decreasing order), the trader can, e.g., buy stocks in the top decile (winners) and short stocks in the bottom decile (losers). 36

This can be a zero-cost strategy, i.e., the corresponding portfolio is dollar-neutral. Alternatively, a long-only portfolio can be constructed by buying stocks in, e.g., the top decile. Once a portfolio is established at t = 0, it is kept unaltered during

a predefined "holding period", 37 which can be 1 month or longer (longer holding period portfolios typically have diminishing returns before trading costs as the momentum effect fades with time). Multi-month-holding portfolios can be constructed by overlapping 1-month-holding portfolios (see, e.g., \[Jegadeesh and Titman, 1993\]).

The above prescription does not fix the relative weights w i of the stocks in the portfolio. For a long-only portfolio we have w i ≥ 0 and

N X $$ i=1 $$ $$ wi = 1 $$ (271)

So, if the total investment level is I, then the stock labeled by i has I × w i dollars invested in it. This, up to rounding, translates into Q i = I × w i /P i (0) shares. 38 One can simply take uniform weights, w i = 1 */N for all stocks, albeit other weighting schemes are possible. E.g., we can have nonuniform w i ∝ 1 */σ i, or w i ∝ 1 */σ 2

*i, etc. For a dollar-neutral portfolio we can have negative w i and

N X $$ i=1 $$ |wi| = 1 (272)

N X $$ i=1 $$ $$ wi = 0 $$ (273)

So, if the total investment level is I = I L + *I S, where I L is the total long investment, and I S is the absolute value of the total short investment, 39 then the stock labeled by i has I × w i dollars invested in it, where w i \> 0 for long stocks, and w i \< 0 for short stocks. One can simply take modulus-uniform weights, where w i = 1 */ 2 *N L for all N L long stocks, and w i = − 1 */ 2 *N S for all N S short stocks. However, other weighting schemes are possible, e.g., as above, weights suppressed by σ i, σ 2 *i, etc. 40

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
