# 5.7 Fifty-fifty butterfly

- Section: 5.7
- Asset class: Fixed income
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

This is a variation of the standard butterfly. In the above notations for the dollarduration-neutral butterfly, we have

P1 D1 = P3 D3 = 1

2 P 2 D 2 (406)

So, the fifty-fifty butterfly is still dollar-duration-neutral, but it is no longer dollarneutral (i.e., it is not a zero-cost strategy). Instead, dollar durations of the wings are the same (hence the term "fifty-fifty"). As a result, the strategy is (approximately) neutral to small steepening and flattening of the yield curve, to wit, if the interest rate spread change between the body and the short-maturity wing is equal to the spread change between the long-maturity wing and the body. That is why this strategy is a.k.a. "neutral curve butterfly" (whose cost is non-dollar-neutrality).

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.7. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Fifty-fifty butterfly: equal dollar durations in both wings (Eq. 406). Long/short.

Proxies and assumptions: Same ETFs and assumed durations as 5.6.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/5.7-fifty-fifty-butterfly/multi.json --out strategies/catalog/5.7-fifty-fifty-butterfly/multi.results.json`.

Compounded over the forward windows: strategy 3.2%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 1 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 0 | 0.58% | 0.00% | 3.82% | 2+1 |
| 2017-07-01..2018-01-01 | 0 | -0.02% | 0.00% | 5.35% | 2+1 |
| 2018-07-01..2019-01-01 | 0 | -0.09% | 0.00% | -2.98% | 2+1 |
| 2019-07-01..2020-01-01 | 0 | 0.26% | 0.00% | 4.57% | 2+1 |
| 2020-07-01..2021-01-01 | 0 | 0.05% | 0.00% | 10.57% | 2+1 |
| 2021-07-01..2022-01-01 | 0 | -0.25% | 0.00% | 5.50% | 2+1 |
| 2022-07-01..2023-01-01 | 0 | 0.28% | 0.00% | 1.21% | 2+1 |
| 2023-07-01..2024-01-01 | 0 | 1.03% | 0.00% | 3.80% | 2+1 |
| 2024-07-01..2025-01-01 | 0 | 0.95% | 0.00% | 3.87% | 2+1 |
| 2025-07-01..2026-01-01 | 0 | 0.40% | 0.00% | 5.47% | 2+1 |
