# 4.6 Multi-asset trend following

- Section: 4.6
- Asset class: Exchange-traded funds
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

One allure of ETFs is their diversification power: ETFs allow to gain exposure to different sectors, countries, asset classes, factors, etc., by taking positions in a relatively small number of ETFs (as opposed to taking positions in a large number of underlying instruments, e.g., thousands of stocks). Here we focus on long-only trend-following portfolios. One needs to determine the weight w i of each ETF. One (but by far not the only) way to fix these weights is as follows. First, as in the sector momentum rotation strategy, we compute cumulative returns R cum*

*i (over some period T, e.g., 6-12 months). We only take ETFs with positive R cum*

*i. If desired, optionally, we can further filter out ETFs as in the sector momentum rotation strategy with an MA filter, by keeping only the ETFs whose last closing prices P i are higher than their corresponding long-term moving averages MA *i ( *T ′) (typically, the MA length T ′ is 100 to 200 days). Now, instead of taking ETFs in the top decile by R cum*

*i (as in the sector momentum rotation strategy), we can assign nonzero weights w i to all remaining ETFs, whose number in this context is relatively small to begin with by design. The weights can, e.g., be assigned as follows: wi = \gamma1 Rcum *i (371) wi = \gamma2 Rcum *i /\sigmai (372) wi = \gamma3 Rcum

Here: σ i is the historical volatility; and the overall normalization coefficients γ 1 , γ 2 , γ 3 in each case are computed based on the requirement that P *N*

i=1 wi = 1 (where N is the number of ETFs in our portfolio after all filters are applied, i.e., those with nonzero weights). Thus, the weights in Eq. (371) are simply proportional to the past cumulative returns R cum*

*i, which are taken as the measure of momentum, so the expected returns are also given by (or, more precisely, proportional to) R cum*

*i. The issue with this weighting scheme is that it overweighs volatile ETFs as on average R cum*

*i \propto\sigmai. The weights in Eq. (372) mitigate this, while the weights in Eq. (373) actually optimize the Sharpe ratio of the ETF portfolio assuming a diagonal covariance matrix C ij = diag( *σ 2

*i) for the ETF returns, i.e., by ignoring their correlations. 83 Imposing bounds w i ≤ w max i can further mitigate overweighing.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.6. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Multi-asset trend following: monthly, hold only assets with positive cumulative return over the lookback, weights proportional to that return (Eq. 371), gross 1. Lookback 126 or 252 days chosen in training. Long only.

Proxies and assumptions: ETFs stand in for futures: SPY, EFA, EEM (equities), TLT, IEF (bonds), GLD, DBC, USO (commodities), UUP, FXE (currencies), VNQ (real estate).

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/4.6-multi-asset-trend-following/multi.json --out strategies/catalog/4.6-multi-asset-trend-following/multi.results.json`.

Compounded over the forward windows: strategy -4.8%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 1 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 126 | 0.00% | 0.00% | 3.82% | 0+0 |
| 2017-07-01..2018-01-01 | 126 | 3.90% | 0.00% | 5.35% | 30+27 |
| 2018-07-01..2019-01-01 | 126 | -5.49% | 0.00% | -2.98% | 20+15 |
| 2019-07-01..2020-01-01 | 252 | 1.70% | 0.00% | 4.57% | 24+21 |
| 2020-07-01..2021-01-01 | 252 | 2.82% | 0.00% | 10.57% | 24+17 |
| 2021-07-01..2022-01-01 | 126 | -1.27% | 0.00% | 5.50% | 28+19 |
| 2022-07-01..2023-01-01 | 252 | -6.15% | 0.00% | 1.21% | 12+7 |
| 2023-07-01..2024-01-01 | 126 | -4.93% | 0.00% | 3.80% | 33+22 |
| 2024-07-01..2025-01-01 | 252 | -0.80% | 0.00% | 3.87% | 33+22 |
| 2025-07-01..2026-01-01 | 252 | 6.14% | 0.00% | 5.47% | 25+21 |
