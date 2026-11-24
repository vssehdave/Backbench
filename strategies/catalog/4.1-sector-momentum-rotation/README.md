# 4.1 Sector momentum rotation

- Section: 4.1
- Asset class: Exchange-traded funds
- Harness status: **tested: cross-sectional harness** (`python money.py xs strategies/catalog/4.1-sector-momentum-rotation/xs_manifest.json`; results in `xs_results.json`) - **survivorship-biased**; see labels below.

## Description (paper)

Empirical evidence suggests that the momentum effect exists not only for individual stocks but also for sectors and industries. 74 A sector momentum rotation strategy is

based on overweighing holdings in outperforming sectors and underweighing holdings in underperforming sectors, where the "outperformance" and "underperformance" are based on momentum during the past T -month formation period (which typically ranges from 6 to 12 months). ETFs concentrated in specific sectors/industries offer a simple way to implement sector/industry rotation without having to buy or sell a large number of underlying stocks. Similarly to Subsection 3.1, as a measure of sector/industry momentum, we can use the corresponding ETF's cumulative return: *cum*

*i $$ (t) = $$ *P i ( *t) *P i ( *t + T) − 1 (361)

Here P i ( *t) is the price of the ETF labeled by i. (As above, t + T is T months in the *past w.r.t. t.) Right after time t, the trader can, e.g., buy the ETFs in the top decile by R cum*

*i ( *t) and hold the portfolio for a holding period (typically 1 to 3 months). Dollar-neutral strategies can also be constructed by, e.g., buying ETFs in the top decile and shorting ETFs in the bottom decile (as stocks, ETFs can be shorted). 75

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## xs harness result

Construction: Long the top-decile sector ETF (one of 11 SPDR ETFs) by 12-month return, monthly.
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: survivorship-biased; survivorship-biased: today's 11 SPDR sector ETFs, thin universe (one ETF held).

Summary over the 9 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | +9.6% | +8.0% | 1.12 |
| equal-weight | +7.3% | +7.2% | 1.38 |
| SPY | +8.8% | +10.9% | 1.52 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.25%, turnover 8.8x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +0.0% | +3.4% | +7.9% | +0.0% | n/a | 0.00% (no trades) |
| 2017-07-03..2017-12-29 | +16.5% | +9.9% | +11.5% | +0.0% | 2.93 | 0.33% |
| 2018-07-02..2018-12-31 | -8.1% | -7.6% | -6.9% | +0.0% | -0.72 | 0.28% |
| 2019-07-01..2019-12-31 | +17.7% | +8.8% | +10.9% | +0.0% | 3.01 | 0.42% |
| 2020-07-01..2020-12-31 | +24.7% | +20.0% | +22.1% | +0.0% | 1.89 | 0.05% |
| 2021-07-01..2021-12-31 | +8.0% | +10.5% | +11.7% | +0.0% | 0.81 | 0.18% |
| 2022-07-01..2022-12-30 | +23.0% | +3.9% | +2.3% | +0.0% | 1.38 | 0.05% |
| 2023-07-03..2023-12-29 | +5.0% | +6.1% | +8.0% | +0.0% | 0.65 | 0.27% |
| 2024-07-01..2024-12-31 | -0.4% | +7.2% | +8.4% | +0.0% | 0.04 | 0.39% |
| 2025-07-01..2025-12-31 | -0.1% | +6.8% | +11.0% | +0.0% | 0.07 | 0.28% |
