# 3.18 Statistical arbitrage - optimization

- Section: 3.18
- Asset class: Stocks
- Harness status: **tested: cross-sectional harness** (`python money.py xs strategies/catalog/3.18-statistical-arbitrage-optimization/xs_manifest.json`; results in `xs_results.json`) - **survivorship-biased**; see labels below.

## Description (paper)

Let C ij be the sample or model covariance matrix for the N stock returns in a

portfolio. 62 Let D i be the dollar holdings in our portfolio. The expected portfolio P&L P, volatility V and Sharpe ratio S are given by

P =

N X $$ i=1 $$

E i D i (342)

V 2 =

N X $$ i,j=1 $$

C ij D i D j (343)

S = P/V (344)

Here E i are the expected stock returns. Instead of the dollar holdings D i, it is more

convenient to work with dimensionless holding weights (which are positive/negative for long/short positions)

wi = Di/I (345)

where I is the total investment level. The holding weights satisfy the condition

N X $$ i=1 $$ |wi| = 1 (346)

We have P = I × e *P, V = I × e *V and S = e *P/ e *V, where eP =

N X $$ i=1 $$ *E i w i (347) $$ eV 2 = $$

N X $$ i,j=1 $$

To determine the portfolio weights w i, often one requires that the Sharpe ratio \[Sharpe, 1966\], \[Sharpe, 1994\] be maximized: *S → max (349)

Assuming no additional conditions on w i (e.g., upper or lower bounds), the solution to Eq. (349) in the absence of trading costs is given by $$ wi = \gamma $$

N X $$ j=1 $$ *− 1 *ij E j (350)

where C − 1 is the inverse of C, and the normalization coefficient γ is determined from Eq. (346) (and γ > 0 so eP > 0). The weights given by Eq. (350) generically do not correspond to a dollar-neutral portfolio. To have a dollar-neutral portfolio, we need to maximize the Sharpe ratio subject to the dollar-neutrality constraint. 3.18.1 Dollar-neutrality

We can achieve dollar-neutrality as follows. In the absence of bounds, trading costs, etc., the Sharpe ratio is invariant under simultaneous rescalings of all holding weights *w i → ζ w i, where ζ \> 0. Due to this scale invariance, the Sharpe ratio maximization problem can be recast in terms of minimizing a quadratic objective function: $$ g(w, \lambda) = \lambda $$

N X $$ i,j=1 $$ *C ij w i w j −*

N X $$ i=1 $$ *E i w i (351) $$ g(w, \lambda) \tomin $$ (352)

where λ \> 0 is a parameter, and minimization is w.r.t. w i. The solution is given by $$ wi = 1 $$ \lambda

N X $$ j=1 $$ *− 1 *ij E j (353)

and λ is fixed via Eq. (346). The objective function approach - which is the meanvariance optimization \[Markowitz, 1952\] - is convenient if we wish to impose linear homogeneous constraints (which do not spoil the aforesaid scale invariance) on w i, e.g., the dollar-neutrality constraint. We introduce a Lagrange multiplier µ: 63 $$ g(w, µ, \lambda) = \lambda $$

N X $$ i,j=1 $$ *C ij w i w j −*

N X $$ i=1 $$ *E i w i − µ*

N X $$ i=1 $$ *i (354) g(w, µ, \lambda) →min (355)

Minimization w.r.t. w i and µ now gives the following equations: \lambda

N X $$ j=1 $$ *C ij w j = E i + µ (356)

N X $$ i=1 $$ $$ wi = 0 $$ (357)

So we have dollar-neutrality. The solution to Eqs. (356) and (357) is given by: $$ wi = 1 $$ \lambda

" N X $$ j=1 $$ *− 1 *ij E j −*

N X $$ j=1 $$ *− 1 *ij*

N k,l=1 C−1 *kl E l N k,l=1 C−1 *kl*

(358)

By construction, w i satisfy the dollar-neutrality constraint (357), and λ is fixed via Eq. (346). The expected returns E i can be based on mean-reversion, momentum, machine learning or other signals. Eq. (358) constructs a dollar-neutral portfolio with "risk management" built in. E.g., the weights w i (roughly) are suppressed by stock volatilities σ i (where σ 2

*i = C ii) assuming that on average \| E i \| are of order σ i. 64

The above implementation of the dollar-neutrality constraint via minimizing the quadratic objective function (354) is equivalent to imposing this constraint in Sharpe ratio maximization as no trading costs, position/trading bounds, nonlinear/inhomogeneous constraints, etc., are present. More generally Sharpe ratio maximization is not equivalent to minimizing a quadratic objective function (see, e.g., \[Kakushadze, 2015b\]), albeit in practice usually the latter approach is used.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.18. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## xs harness result

Construction: Dollar-neutral mean-variance weights, eq. 358, diagonal covariance, 12-1 momentum as expected return.
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: proxy: diagonal covariance, momentum as expected return; survivorship-biased; survivorship-biased S&P 500 universe.

Summary over the 9 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | -1.0% | -0.2% | -0.07 |
| equal-weight | +8.0% | +7.6% | 1.24 |
| SPY | +8.8% | +10.9% | 1.52 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.39%, turnover 6.2x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +0.0% | +8.8% | +7.9% | +0.0% | n/a | 0.00% (no trades) |
| 2017-07-03..2017-12-29 | +2.1% | +9.9% | +11.5% | +0.0% | 0.93 | 0.40% |
| 2018-07-02..2018-12-31 | -0.2% | -9.1% | -6.9% | +0.0% | -0.04 | 0.39% |
| 2019-07-01..2019-12-31 | -3.9% | +8.2% | +10.9% | +0.0% | -0.9 | 0.38% |
| 2020-07-01..2020-12-31 | -7.2% | +26.7% | +22.1% | +0.0% | -0.84 | 0.38% |
| 2021-07-01..2021-12-31 | -1.6% | +8.6% | +11.7% | +0.0% | -0.43 | 0.39% |
| 2022-07-01..2022-12-30 | +0.8% | +6.3% | +2.3% | +0.0% | 0.22 | 0.38% |
| 2023-07-03..2023-12-29 | -1.1% | +6.4% | +8.0% | +0.0% | -0.36 | 0.39% |
| 2024-07-01..2024-12-31 | +0.4% | +7.6% | +8.4% | +0.0% | 0.16 | 0.39% |
| 2025-07-01..2025-12-31 | +2.0% | +7.2% | +11.0% | +0.0% | 0.63 | 0.40% |
