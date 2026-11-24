# 5.4 Ladders

- Section: 5.4
- Asset class: Fixed income
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

A ladder is a bond portfolio with (roughly) equal capital allocations into bonds of n different maturities T i, i = 1 ,..., n (where the number of rungs n is sizable, e.g., n = 10). The maturities are equidistant: T i +1 = T i + δ. This is a durationtargeting strategy, 89 which maintains an approximately constant duration by selling shorter-maturity bonds as they approach maturity and replacing them with new longer-maturity bonds. A ladder portfolio aims to diversify the interest rate and reinvestment risks 90 by avoiding exposure to only a few maturities (as in bullets and barbells). It also generates a regular revenue stream from the coupons of each bond. The maturity of a ladder portfolio can be defined as the average maturity:

T = 1 *n n X $$ i=1 $$ *i (395)

The income is higher for higher values of T; however, so is the interest rate risk.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.4. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Ladder: equal capital in SHY, IEF and TLT, monthly.

Proxies and assumptions: Three ETFs stand in for ten rungs.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/5.4-ladders/multi.json --out strategies/catalog/5.4-ladders/multi.results.json`.

Compounded over the forward windows: strategy -3.2%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 1 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 0 | -3.68% | 0.00% | 3.82% | 3+0 |
| 2017-07-01..2018-01-01 | 0 | 0.41% | 0.00% | 5.35% | 3+0 |
| 2018-07-01..2019-01-01 | 0 | 0.90% | 0.00% | -2.98% | 3+0 |
| 2019-07-01..2020-01-01 | 0 | 0.87% | 0.00% | 4.57% | 3+0 |
| 2020-07-01..2021-01-01 | 0 | -0.56% | 0.00% | 10.57% | 3+0 |
| 2021-07-01..2022-01-01 | 0 | 0.47% | 0.00% | 5.50% | 3+0 |
| 2022-07-01..2023-01-01 | 0 | -3.34% | 0.00% | 1.21% | 3+0 |
| 2023-07-01..2024-01-01 | 0 | 0.45% | 0.00% | 3.80% | 3+0 |
| 2024-07-01..2025-01-01 | 0 | 0.44% | 0.00% | 3.87% | 3+0 |
| 2025-07-01..2026-01-01 | 0 | 0.96% | 0.00% | 5.47% | 3+0 |
