# 3.10 Mean-reversion - weighted regression

- Section: 3.10
- Asset class: Stocks
- Harness status: **tested: cross-sectional harness** (`python money.py xs strategies/catalog/3.10-mean-reversion-weighted-regression/xs_manifest.json`; results in `xs_results.json`) - **survivorship-biased**; see labels below.

## Description (paper)

Mean-reversion - weighted regression

The conditions (310) satisfied by the demeaned returns when the loadings matrix is binary simply mean that these returns are cluster-neutral, i.e., orthogonal to the K N -vectors v ( *A) comprising the columns of Λ *iA. Such orthogonality can be defined for any loadings matrix, not just a binary one. So, we can consider a generalization where the loadings matrix, call it Ω *iA, may have some binary columns, but generally it need not. The binary columns, if any, can, e.g., be industry (or sector) based risk factors; the non-binary columns are interpreted as some non-industry based risk factors; and the orthogonality condition

N X $$ i=1 $$

e *R i Ω *iA , A = 1 ,..., K (313)

can be satisfied if the twiddled returns e *R i are related to the residuals ε i of the regression of R i over Ω *iA with some (generally nonuniform) regression weights z i via

$$ eR = Z \epsilon $$ (314) \epsilon = R −ΩQ−1 ΩT Z R (315) Z = diag(zi) (316) *Q = Ω *T Z Ω (317)

If the intercept is included in Ω *iA (i.e., a linear combination of the columns of Ω *iA equals the unit N -vector ν), then we automatically have

N X $$ i=1 $$ $$ eRi = 0 $$ (318)

The weights z i can, e.g., be taken as z i = 1 */σ 2

*i, where σ i are historical volatilities. 54

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.10. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## xs harness result

Construction: Weighted-regression residuals on sector dummies, weights 1/variance (eq. 314), positions minus the twiddled return.
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: proxy: current GICS sectors as the only regressors (lookahead, ex-members dropped); survivorship-biased; survivorship-biased S&P 500 universe.

Summary over the 9 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | -1.5% | -1.5% | -0.75 |
| equal-weight | +8.0% | +7.6% | 1.24 |
| SPY | +8.8% | +10.9% | 1.52 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.63%, turnover 16.0x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +0.0% | +8.8% | +7.9% | +0.0% | n/a | 0.00% (no trades) |
| 2017-07-03..2017-12-29 | -0.6% | +9.9% | +11.5% | +0.0% | -0.57 | 0.63% |
| 2018-07-02..2018-12-31 | -0.2% | -9.1% | -6.9% | +0.0% | -0.12 | 0.64% |
| 2019-07-01..2019-12-31 | -1.5% | +8.2% | +10.9% | +0.0% | -0.63 | 0.63% |
| 2020-07-01..2020-12-31 | -2.5% | +26.7% | +22.1% | +0.0% | -1.04 | 0.64% |
| 2021-07-01..2021-12-31 | -3.1% | +8.6% | +11.7% | +0.0% | -1.43 | 0.60% |
| 2022-07-01..2022-12-30 | +1.9% | +6.3% | +2.3% | +0.0% | 0.86 | 0.66% |
| 2023-07-03..2023-12-29 | -0.6% | +6.4% | +8.0% | +0.0% | -0.31 | 0.64% |
| 2024-07-01..2024-12-31 | -3.0% | +7.6% | +8.4% | +0.0% | -1.55 | 0.63% |
| 2025-07-01..2025-12-31 | -3.8% | +7.2% | +11.0% | +0.0% | -1.93 | 0.62% |
