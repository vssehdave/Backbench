# 3.7 Residual momentum

- Section: 3.7
- Asset class: Stocks
- Harness status: **tested: cross-sectional harness** (`python money.py xs strategies/catalog/3.7-residual-momentum/xs_manifest.json`; results in `xs_results.json`) - **survivorship-biased**; see labels below.

## Description (paper)

This is the same as the price-momentum strategy with the stock returns R i ( *t) replaced by the residuals ϵ i ( *t) of a serial regression of the stock returns R i ( *t) over, e.g., the 3 Fama-French factors MKT( *t), SMB( *t), HML( *t), 50 with the intercept (see,

47 Another approach is to fix the weights w A by optimizing a portfolio of the F expected returns corresponding to the F factors (using an invertible F × F covariance matrix for these returns).

$$ Ri(t) = \alphai + \beta1,i MKT(t) + \beta2,i SMB(t) + \beta3,i HML(t) + ϵi(t) $$ (278)

The regression is run over a 36-month period \[Blitz, Huij and Martens, 2011\] (with the 1-month skip period) to estimate the regression coefficients α i, β 1 ,i, β 2 ,i, β 3 ,i. Once the coefficients are estimated, the residuals can be computed for the 12-month formation period (again, with the 1-month skip period):

ϵi(t) = Ri(t) −\beta1,i MKT(t) −\beta2,i SMB(t) −\beta3,i HML(t) (279)

Note that α i is not included in this computation of the residuals for the 12-month formation period as α i was computed for the 36-month period. These residuals *ϵ i ( *t) are then used to compute, e.g., the risk-adjusted residual returns e *R risk.adj*

*i (here *S = 1 and T = 12; the holding period typically is 1 month, but can be longer): *mean i $$ = 1 $$

T

S + T − 1 X t=S *ϵ i ( *t) (280) e *R risk.adj i = ϵ mean i e\sigmai (281) e\sigma2 $$ i = $$ *T − 1

S + T − 1 X t=S ( *ϵ i ( *t) − ϵ mean i) 2 (282)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.7. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## xs harness result

Construction: 12-1 momentum on residuals of a 36-month regression, standardised by residual volatility, decile long/short.
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: proxy: market-only regression (equal-weight universe), no SMB/HML; survivorship-biased; survivorship-biased S&P 500 universe.

Summary over the 7 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | -1.8% | -0.9% | -0.18 |
| equal-weight | +10.1% | +7.6% | 1.34 |
| SPY | +10.6% | +10.9% | 1.55 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.38%, turnover 8.5x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +0.0% | +8.8% | +7.9% | +0.0% | n/a | 0.00% (no trades) |
| 2017-07-03..2017-12-29 | +0.0% | +9.9% | +11.5% | +0.0% | n/a | 0.00% (no trades) |
| 2018-07-02..2018-12-31 | +0.0% | -9.1% | -6.9% | +0.0% | n/a | 0.00% (no trades) |
| 2019-07-01..2019-12-31 | -5.6% | +8.2% | +10.9% | +0.0% | -0.81 | 0.38% |
| 2020-07-01..2020-12-31 | -9.4% | +26.7% | +22.1% | +0.0% | -0.7 | 0.40% |
| 2021-07-01..2021-12-31 | -0.9% | +8.6% | +11.7% | +0.0% | -0.33 | 0.38% |
| 2022-07-01..2022-12-30 | +3.9% | +6.3% | +2.3% | +0.0% | 0.66 | 0.36% |
| 2023-07-03..2023-12-29 | -2.5% | +6.4% | +8.0% | +0.0% | -0.59 | 0.38% |
| 2024-07-01..2024-12-31 | -0.2% | +7.6% | +8.4% | +0.0% | -0.01 | 0.39% |
| 2025-07-01..2025-12-31 | +2.2% | +7.2% | +11.0% | +0.0% | 0.51 | 0.37% |
