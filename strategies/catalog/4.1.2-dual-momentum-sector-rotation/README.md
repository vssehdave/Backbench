# 4.1.2 Dual-momentum sector rotation

- Section: 4.1.2
- Asset class: Exchange-traded funds
- Harness status: **tested: cross-sectional harness** (`python money.py xs strategies/catalog/4.1.2-dual-momentum-sector-rotation/xs_manifest.json`; results in `xs_results.json`) - **survivorship-biased**; see labels below.

## Description (paper)

In long-only strategies, to mitigate the risk of buying ETFs when the broad market is trending down, relative (i.e., cross-sectional) momentum of sector ETFs can be augmented by the absolute (i.e., time-series) momentum of, e.g., a broad market index ETF (see, e.g., \[Antonacci, 2014\], \[Antonacci, 2017\]). 76 So, a long position based on the sector rotation signal (discussed above) is established only if the broad

market index has an upward trend; otherwise, the total available funds are invested into an ETF (e.g., gold or Treasury ETF) uncorrelated with the broad market index: Rule = (

Buy top-decile ETFs if P \> MA( *T ′) Buy an uncorrelated ETF if P ≤ MA( *T ′) (363)

Here P is the broad market index ETF's price at the time of the transaction, and MA( *T ′) is the moving average of this ETF's price. Typically, T ′ is 100 to 200 days.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.1.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## xs harness result

Construction: As 4.1 while SPY is above its 200-day average, otherwise GLD.
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: safe asset chosen: GLD; survivorship-biased; survivorship-biased: today's 11 SPDR sector ETFs, thin universe (one ETF held).

Summary over the 9 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | +6.2% | +3.1% | 0.87 |
| equal-weight | +7.4% | +8.7% | 1.51 |
| SPY | +8.8% | +10.9% | 1.52 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.29%, turnover 10.1x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +0.0% | +1.9% | +7.9% | +0.0% | n/a | 0.00% (no trades) |
| 2017-07-03..2017-12-29 | +16.5% | +9.5% | +11.5% | +0.0% | 2.93 | 0.33% |
| 2018-07-02..2018-12-31 | -10.4% | -6.8% | -6.9% | +0.0% | -1.1 | 0.39% |
| 2019-07-01..2019-12-31 | +17.7% | +8.7% | +10.9% | +0.0% | 3.01 | 0.42% |
| 2020-07-01..2020-12-31 | +24.7% | +18.8% | +22.1% | +0.0% | 1.89 | 0.05% |
| 2021-07-01..2021-12-31 | +8.0% | +9.9% | +11.7% | +0.0% | 0.81 | 0.18% |
| 2022-07-01..2022-12-30 | -3.2% | +3.6% | +2.3% | +0.0% | -0.26 | 0.16% |
| 2023-07-03..2023-12-29 | +3.1% | +6.2% | +8.0% | +0.0% | 0.44 | 0.37% |
| 2024-07-01..2024-12-31 | -0.4% | +7.7% | +8.4% | +0.0% | 0.04 | 0.39% |
| 2025-07-01..2025-12-31 | -0.1% | +8.7% | +11.0% | +0.0% | 0.07 | 0.28% |
