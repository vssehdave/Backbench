# 3.4 Low-volatility anomaly

- Section: 3.4
- Asset class: Stocks
- Harness status: **tested: cross-sectional harness** (`python money.py xs strategies/catalog/3.4-low-volatility-anomaly/xs_manifest.json`; results in `xs_results.json`) - **survivorship-biased**; see labels below.

## Description (paper)

This strategy is based on the empirical observation that future returns of previously low-return-volatility portfolios outperform those of previously high-return-volatility portfolios, 44 which goes counter to the "na¨ıve" expectation that higher risk assets

should yield proportionately higher returns. Thus, if σ i is defined as the historical volatility (computed over a time series of historical returns, as in Eq. (270)), the trader can, e.g., construct a dollar-neutral portfolio by buying stocks in the bottom decile by σ i (low-volatility stocks), and shorting stocks in the top decile (high-volatility stocks). The length of the sample used for computing the historical volatility can, e.g., be 6 months (126 trading days) to a year (252 trading days), with a similar duration for the holding period (with no "skip period" required).

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.4. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## xs harness result

Construction: Long the lowest-volatility decile and short the highest, 252-session daily-return standard deviation, equal weights, dollar neutral.
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: survivorship-biased; survivorship-biased S&P 500 universe.

Summary over the 9 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | -2.7% | -2.9% | -0.28 |
| equal-weight | +8.0% | +7.6% | 1.24 |
| SPY | +8.8% | +10.9% | 1.52 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.27%, turnover 4.5x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +0.0% | +8.8% | +7.9% | +0.0% | n/a | 0.00% (no trades) |
| 2017-07-03..2017-12-29 | -4.0% | +9.9% | +11.5% | +0.0% | -1.22 | 0.28% |
| 2018-07-02..2018-12-31 | +11.8% | -9.1% | -6.9% | +0.0% | 2.33 | 0.26% |
| 2019-07-01..2019-12-31 | -2.0% | +8.2% | +10.9% | +0.0% | -0.28 | 0.28% |
| 2020-07-01..2020-12-31 | -16.3% | +26.7% | +22.1% | +0.0% | -1.36 | 0.27% |
| 2021-07-01..2021-12-31 | +5.4% | +8.6% | +11.7% | +0.0% | 0.88 | 0.27% |
| 2022-07-01..2022-12-30 | -2.9% | +6.3% | +2.3% | +0.0% | -0.29 | 0.25% |
| 2023-07-03..2023-12-29 | -4.3% | +6.4% | +8.0% | +0.0% | -0.7 | 0.27% |
| 2024-07-01..2024-12-31 | -1.2% | +7.6% | +8.4% | +0.0% | -0.17 | 0.28% |
| 2025-07-01..2025-12-31 | -10.7% | +7.2% | +11.0% | +0.0% | -1.72 | 0.25% |
