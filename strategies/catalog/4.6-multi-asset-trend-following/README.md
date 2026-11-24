# 4.6 Multi-asset trend following

- Section: 4.6
- Asset class: Exchange-traded funds
- Harness status: **not testable: multiple instruments** - weights a basket of ETFs by momentum and volatility; needs several series at once.

## Description (paper)

One allure of ETFs is their diversification power: ETFs allow to gain exposure to different sectors, countries, asset classes, factors, etc., by taking positions in a relatively small number of ETFs (as opposed to taking positions in a large number of underlying instruments, e.g., thousands of stocks). Here we focus on long-only trend-following portfolios. One needs to determine the weight w i of each ETF. One (but by far not the only) way to fix these weights is as follows. First, as in the sector momentum rotation strategy, we compute cumulative returns R cum*

*i (over some period T, e.g., 6-12 months). We only take ETFs with positive R cum*

*i. If desired, optionally, we can further filter out ETFs as in the sector momentum rotation strategy with an MA filter, by keeping only the ETFs whose last closing prices P i are higher than their corresponding long-term moving averages MA *i ( *T ′) (typically, the MA length T ′ is 100 to 200 days). Now, instead of taking ETFs in the top decile by R cum*

*i (as in the sector momentum rotation strategy), we can assign nonzero weights w i to all remaining ETFs, whose number in this context is relatively small to begin with by design. The weights can, e.g., be assigned as follows: wi = \gamma1 Rcum *i (371) wi = \gamma2 Rcum *i /\sigmai (372) wi = \gamma3 Rcum

Here: σ i is the historical volatility; and the overall normalization coefficients γ 1 , γ 2 , γ 3 in each case are computed based on the requirement that P *N*

i=1 wi = 1 (where N is the number of ETFs in our portfolio after all filters are applied, i.e., those with nonzero weights). Thus, the weights in Eq. (371) are simply proportional to the past cumulative returns R cum*

*i, which are taken as the measure of momentum, so the expected returns are also given by (or, more precisely, proportional to) R cum*

*i. The issue with this weighting scheme is that it overweighs volatile ETFs as on average R cum*

*i \propto\sigmai. The weights in Eq. (372) mitigate this, while the weights in Eq. (373) actually optimize the Sharpe ratio of the ETF portfolio assuming a diagonal covariance matrix C ij = diag( *σ 2

*i) for the ETF returns, i.e., by ignoring their correlations. 83 Imposing bounds w i ≤ w max i can further mitigate overweighing.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.6. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.
