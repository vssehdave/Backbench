# 3.9 Mean-reversion - single cluster

- Section: 3.9
- Asset class: Stocks
- Harness status: **tested: cross-sectional harness** (`python money.py xs strategies/catalog/3.9-mean-reversion-single-cluster/xs_manifest.json`; results in `xs_results.json`) - **survivorship-biased**; see labels below.

## Description (paper)

This is a generalization of the pairs trading strategy to N \> 2 stocks that are historically highly correlated (e.g., stocks belonging to the same industry or sector). Let R i, i = 1 ,..., N, be the returns for these N stocks: *R i = ln  *P i ( *t 2 ) *P i ( *t 1 )  (292)

R = 1

N

N X $$ i=1 $$ *i (293) e *R i = R i − R (294)

Following the pairs trading intuition, we can short stocks with positive e *R i and buy stocks with negative e *R i. We have the following conditions:

N X $$ i=1 $$ *P i \| Q i \| = I (295)

N X $$ i=1 $$ Pi Qi = 0 (296)

Here: I is the total desired dollar investment; Eq. (296) is the dollar-neutrality constraint; Q i \< 0 for short-sales; Q i \> 0 for buys; P i are the prices at the time the position is established. We have 2 equations and N \> 2 unknowns. A simple prescription (which is one out of myriad possibilities) for specifying Q i is to have the dollar positions D i = P i Q i proportional to the demeaned returns: Di = −\gamma eRi (297)

where γ \> 0 (recall that we short e *R i \> 0 stocks and buy e *R i \< 0 stocks). Then Eq. (296) is automatically satisfied, while Eq. (295) fixes γ: $$ \gamma = $$ *I N $$ i=1 $$ e *R i (298)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.9. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## xs harness result

Construction: Positions proportional to minus the demeaned 1-month log return (eq. 297), the whole universe as one cluster, sum of |weights| = 1.
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: survivorship-biased; survivorship-biased S&P 500 universe; whole universe treated as one cluster; 1-month formation window.

Summary over the 10 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | -1.5% | -1.3% | -0.4 |
| equal-weight | +8.1% | +7.9% | 1.28 |
| SPY | +8.7% | +9.6% | 1.54 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.66%, turnover 16.2x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +2.3% | +8.8% | +7.9% | +0.0% | 1.07 | 0.69% |
| 2017-07-03..2017-12-29 | -0.2% | +9.9% | +11.5% | +0.0% | -0.08 | 0.68% |
| 2018-07-02..2018-12-31 | +0.7% | -9.1% | -6.9% | +0.0% | 0.32 | 0.68% |
| 2019-07-01..2019-12-31 | +0.6% | +8.2% | +10.9% | +0.0% | 0.21 | 0.67% |
| 2020-07-01..2020-12-31 | -2.4% | +26.7% | +22.1% | +0.0% | -0.64 | 0.68% |
| 2021-07-01..2021-12-31 | -5.2% | +8.6% | +11.7% | +0.0% | -1.42 | 0.62% |
| 2022-07-01..2022-12-30 | +0.2% | +6.3% | +2.3% | +0.0% | 0.08 | 0.68% |
| 2023-07-03..2023-12-29 | -2.4% | +6.4% | +8.0% | +0.0% | -0.86 | 0.65% |
| 2024-07-01..2024-12-31 | -4.6% | +7.6% | +8.4% | +0.0% | -1.43 | 0.65% |
| 2025-07-01..2025-12-31 | -3.9% | +7.2% | +11.0% | +0.0% | -1.2 | 0.64% |
