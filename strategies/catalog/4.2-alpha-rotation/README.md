# 4.2 Alpha rotation

- Section: 4.2
- Asset class: Exchange-traded funds
- Harness status: **tested: cross-sectional harness** (`python money.py xs strategies/catalog/4.2-alpha-rotation/xs_manifest.json`; results in `xs_results.json`) - **survivorship-biased**; see labels below.

## Description (paper)

This is the same as the sector momentum rotation strategy with the cumulative ETF returns R cum*

*i replaced by ETF alphas α i, which are the regression coefficients corresponding to the intercept in a serial regression of the ETF returns 77 R i ( *t) over, e.g., the 3 Fama-French factors MKT( *t), SMB( *t), HML( *t) (see fn. 50): 78

$$ Ri(t) = \alphai + \beta1,i MKT(t) + \beta2,i SMB(t) + \beta3,i HML(t) + ϵi(t) $$ (364)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## xs harness result

Construction: As 4.1 with the 3-factor regression intercept (252 sessions) as the ranking variable.
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: proxy: ETF-mimicking factors (SPY, IWM-SPY, IVE-IVW) instead of Fama-French; survivorship-biased; survivorship-biased: today's 11 SPDR sector ETFs, thin universe (one ETF held).

Summary over the 9 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | +4.5% | +5.6% | 0.4 |
| equal-weight | +7.3% | +7.2% | 1.38 |
| SPY | +8.8% | +10.9% | 1.52 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.29%, turnover 10.4x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +0.0% | +3.4% | +7.9% | +0.0% | n/a | 0.00% (no trades) |
| 2017-07-03..2017-12-29 | +5.6% | +9.9% | +11.5% | +0.0% | 1.08 | 0.55% |
| 2018-07-02..2018-12-31 | -15.0% | -7.6% | -6.9% | +0.0% | -1.44 | 0.27% |
| 2019-07-01..2019-12-31 | +7.2% | +8.8% | +10.9% | +0.0% | 1.14 | 0.06% |
| 2020-07-01..2020-12-31 | +18.3% | +20.0% | +22.1% | +0.0% | 1.62 | 0.29% |
| 2021-07-01..2021-12-31 | +10.1% | +10.5% | +11.7% | +0.0% | 1.01 | 0.30% |
| 2022-07-01..2022-12-30 | +23.0% | +3.9% | +2.3% | +0.0% | 1.38 | 0.05% |
| 2023-07-03..2023-12-29 | +1.6% | +6.1% | +8.0% | +0.0% | 0.27 | 0.26% |
| 2024-07-01..2024-12-31 | -2.4% | +7.2% | +8.4% | +0.0% | -0.22 | 0.29% |
| 2025-07-01..2025-12-31 | -8.1% | +6.8% | +11.0% | +0.0% | -1.24 | 0.58% |
