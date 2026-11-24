# 5.8.1 Maturity-weighted butterfly

- Section: 5.8.1
- Asset class: Fixed income
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

This is a variation of the regression-weighted butterfly, where instead of fixing β in Eq. (408) via a regression based on historical data, this coefficient is based on the 3 bond maturities: $$ \beta = T2 −T1 $$

T 3 − T 2 (409)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.8.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Maturity-weighted butterfly: curve-neutral with beta=(T2-T1)/(T3-T2), maturities 2, 8.5, 25 years assumed (Eqs. 407-408). Long/short.

Proxies and assumptions: Same ETFs and assumed durations as 5.6.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/5.8.1-maturity-weighted-butterfly/multi.json --out strategies/catalog/5.8.1-maturity-weighted-butterfly/multi.results.json`.

Compounded over the forward windows: strategy 0.7%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 1 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 0 | 0.44% | 0.00% | 3.82% | 2+1 |
| 2017-07-01..2018-01-01 | 0 | 0.06% | 0.00% | 5.35% | 2+1 |
| 2018-07-01..2019-01-01 | 0 | -0.39% | 0.00% | -2.98% | 2+1 |
| 2019-07-01..2020-01-01 | 0 | 0.10% | 0.00% | 4.57% | 2+1 |
| 2020-07-01..2021-01-01 | 0 | -0.03% | 0.00% | 10.57% | 2+1 |
| 2021-07-01..2022-01-01 | 0 | -0.03% | 0.00% | 5.50% | 2+1 |
| 2022-07-01..2023-01-01 | 0 | 0.16% | 0.00% | 1.21% | 2+1 |
| 2023-07-01..2024-01-01 | 0 | 0.24% | 0.00% | 3.80% | 2+1 |
| 2024-07-01..2025-01-01 | 0 | 0.26% | 0.00% | 3.87% | 2+1 |
| 2025-07-01..2026-01-01 | 0 | -0.08% | 0.00% | 5.47% | 2+1 |
