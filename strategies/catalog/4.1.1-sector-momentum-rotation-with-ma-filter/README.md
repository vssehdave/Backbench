# 4.1.1 Sector momentum rotation with MA filter

- Section: 4.1.1
- Asset class: Exchange-traded funds
- Harness status: **tested: cross-sectional harness** (`python money.py xs strategies/catalog/4.1.1-sector-momentum-rotation-with-ma-filter/xs_manifest.json`; results in `xs_results.json`) - **survivorship-biased**; see labels below.

## Description (paper)

This is a variation/refinement of the sector momentum rotation strategy. An ETF in the top (bottom) decile is bought (sold) only if it passes an additional filter based on a moving average MA( *T ′) of this ETF's price: Rule = (

Buy top-decile ETFs only if P \> MA( *T ′) Short bottom-decile ETFs only if P \< MA( *T ′) (362)

Here P is the ETF's price at the time of the transaction, and MA( *T ′) is computed using daily prices ( *T ′ can but need not be equal T; e.g., T ′ can be 100 to 200 days).

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.1.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## xs harness result

Construction: As 4.1, but cash when the chosen ETF is under its 200-day average.
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: survivorship-biased; survivorship-biased: today's 11 SPDR sector ETFs, thin universe (one ETF held).

Summary over the 9 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | +7.1% | +5.0% | 0.96 |
| equal-weight | +7.3% | +7.2% | 1.38 |
| SPY | +8.8% | +10.9% | 1.52 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.26%, turnover 9.3x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +0.0% | +3.4% | +7.9% | +0.0% | n/a | 0.00% (no trades) |
| 2017-07-03..2017-12-29 | +16.5% | +9.9% | +11.5% | +0.0% | 2.93 | 0.33% |
| 2018-07-02..2018-12-31 | -10.1% | -7.6% | -6.9% | +0.0% | -1.09 | 0.28% |
| 2019-07-01..2019-12-31 | +17.7% | +8.8% | +10.9% | +0.0% | 3.01 | 0.42% |
| 2020-07-01..2020-12-31 | +24.7% | +20.0% | +22.1% | +0.0% | 1.89 | 0.05% |
| 2021-07-01..2021-12-31 | +8.0% | +10.5% | +11.7% | +0.0% | 0.81 | 0.18% |
| 2022-07-01..2022-12-30 | +2.9% | +3.9% | +2.3% | +0.0% | 0.34 | 0.17% |
| 2023-07-03..2023-12-29 | +5.0% | +6.1% | +8.0% | +0.0% | 0.65 | 0.27% |
| 2024-07-01..2024-12-31 | -0.4% | +7.2% | +8.4% | +0.0% | 0.04 | 0.39% |
| 2025-07-01..2025-12-31 | -0.1% | +6.8% | +11.0% | +0.0% | 0.07 | 0.28% |
