# 9.3 Portfolio diversification with commodities

- Section: 9.3
- Asset class: Commodities
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

Commodity markets typically have a low correlation with equity markets, which can be used to improve performance characteristics of equity portfolios by combining equity and commodity investments. There are different ways to do this. A "passive approach" would amount to buying commodities with a preset portion of the available funds, holding them, and rebalancing the portfolio with some periodicity (e.g., monthly or annually). An "active approach" would amount to a tactical asset allocation approach via increasing/decreasing the exposure to commodities based on an increase/decrease in the Fed discount rate (empirically, commodity returns tend to be sizably correlated with the Fed monetary policy) or some other methodology. 154

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 9.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Passive commodity diversification: 90% SPY, 10% DBC, monthly rebalance.

Proxies and assumptions: DBC stands in for a commodity futures index; the 90/10 split is my assumption (the paper gives none).

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/9.3-portfolio-diversification-with-commodities/multi.json --out strategies/catalog/9.3-portfolio-diversification-with-commodities/multi.results.json`.

Compounded over the forward windows: strategy 44.8%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 1 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 0 | 3.68% | 0.00% | 3.82% | 2+0 |
| 2017-07-01..2018-01-01 | 0 | 5.59% | 0.00% | 5.35% | 2+0 |
| 2018-07-01..2019-01-01 | 0 | -3.43% | 0.00% | -2.98% | 2+0 |
| 2019-07-01..2020-01-01 | 0 | 4.40% | 0.00% | 4.57% | 2+0 |
| 2020-07-01..2021-01-01 | 0 | 10.25% | 0.00% | 10.57% | 2+0 |
| 2021-07-01..2022-01-01 | 0 | 5.34% | 0.00% | 5.50% | 2+0 |
| 2022-07-01..2023-01-01 | 0 | 0.62% | 0.00% | 1.21% | 2+0 |
| 2023-07-01..2024-01-01 | 0 | 3.51% | 0.00% | 3.80% | 2+0 |
| 2024-07-01..2025-01-01 | 0 | 3.25% | 0.00% | 3.87% | 2+0 |
| 2025-07-01..2026-01-01 | 0 | 5.06% | 0.00% | 5.47% | 2+0 |
