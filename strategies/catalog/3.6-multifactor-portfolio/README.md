# 3.6 Multifactor portfolio

- Section: 3.6
- Asset class: Stocks
- Harness status: **tested: cross-sectional harness** (`python money.py xs strategies/catalog/3.6-multifactor-portfolio/xs_manifest.json`; results in `xs_results.json`) - **survivorship-biased**; see labels below.

## Description (paper)

This strategy amounts to buying and shorting stocks based on multiple factors such as value, momentum, etc. For instance, usually value and momentum are negatively correlated and combining them can add value (see, e.g., \[Asness, Moskowitz and Pedersen, 2013\]). There is a variety of ways in which F \> 1 factors can be combined. 46 The simplest way is to diversify the exposure to the F factors with some weights w A, where A = 1 ,..., F labels the factors. That is, if I is the total investment level, then the F portfolios (each built as above based on the corresponding factor) are allocated the investment levels I A = w A × I, where (assuming all w A \> 0)

F X

A=1

Thus, one can simply take uniform weights w A = 1 */F, albeit this may not be the most optimal weighting scheme. E.g., similarly to Subsection 3.1, there are weighting

Thorley, 2010\], \[Frazzini and Pedersen, 2014\], \[Fu, 2009\], \[Garcia-Feij´oo et al, 2015\], \[Li, Sullivan and Garcia-Feij´oo, 2014\], \[Li, Sullivan and Garcia-Feij´oo, 2016\], \[Merton, 1987\].

schemes with wA \propto1/\sigmaA, wA \propto1/\sigma2

*A, etc., where σ A is the historical volatility for the corresponding factor portfolio (uniformly normalized, e.g., per dollar invested). 47

Alternatively, consider F rankings of stocks based on the F factors. One can now combine these rankings in various ways to blend the factors. E.g., in the case of two factors, momentum and value, one can take the top (winners) and bottom (losers) quintiles by momentum and further split them into top half and bottom half, respectively, by value. Or one can take the top and bottom quintiles by value and split them by momentum. 48 Yet another way is to define demeaned ranks sAi = rank(fAi) −1

N

N X $$ j=1 $$ rank( *f Aj) (276)

where f Ai is the numeric value of the factor labeled by A (e.g., momentum) for the stock labeled by i ( *i = 1 ,..., N). One can then simply average the ranks: $$ si = 1 $$

F

F X

A=1 *Ai (277)

The combined "score" s i can have ties, which, if need be (e.g., if there is an ambiguity at the border of the top decile) can be resolved, e.g., simply by giving preference to one of the factor rankings. Averaging over s Ai simply minimizes the sum of squares of the Euclidean distances between the N -vector s i and the K N -vectors s Ai. One can introduce nonuniform weights into this sum (which would amount to a weighted average in Eq. (277)), or even use a different definition of the distance (e.g., the Manhattan distance), which would complicate the problem computationally. Etc. 49

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.6. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## xs harness result

Construction: Average of the ranks of two factors, long the top decile, short the bottom. Paper pair is value and momentum; here momentum (12-1) and low volatility.
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: proxy: momentum + low volatility, value is not available; survivorship-biased; survivorship-biased S&P 500 universe.

Summary over the 9 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | -2.0% | -2.8% | 0.1 |
| equal-weight | +8.0% | +7.6% | 1.24 |
| SPY | +8.8% | +10.9% | 1.52 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.33%, turnover 6.7x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +0.0% | +8.8% | +7.9% | +0.0% | n/a | 0.00% (no trades) |
| 2017-07-03..2017-12-29 | -0.6% | +9.9% | +11.5% | +0.0% | -0.12 | 0.34% |
| 2018-07-02..2018-12-31 | +9.3% | -9.1% | -6.9% | +0.0% | 2.85 | 0.34% |
| 2019-07-01..2019-12-31 | -3.7% | +8.2% | +10.9% | +0.0% | -0.49 | 0.32% |
| 2020-07-01..2020-12-31 | -17.4% | +26.7% | +22.1% | +0.0% | -1.24 | 0.32% |
| 2021-07-01..2021-12-31 | +2.9% | +8.6% | +11.7% | +0.0% | 0.88 | 0.38% |
| 2022-07-01..2022-12-30 | -2.8% | +6.3% | +2.3% | +0.0% | -0.25 | 0.31% |
| 2023-07-03..2023-12-29 | -4.2% | +6.4% | +8.0% | +0.0% | -0.67 | 0.34% |
| 2024-07-01..2024-12-31 | +3.0% | +7.6% | +8.4% | +0.0% | 0.76 | 0.34% |
| 2025-07-01..2025-12-31 | -4.6% | +7.2% | +11.0% | +0.0% | -0.85 | 0.34% |
