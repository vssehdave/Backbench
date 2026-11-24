# 4.1.1 Sector momentum rotation with MA filter

- Section: 4.1.1
- Asset class: Exchange-traded funds
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

This is a variation/refinement of the sector momentum rotation strategy. An ETF in the top (bottom) decile is bought (sold) only if it passes an additional filter based on a moving average MA( *T ′) of this ETF's price: Rule = (

Buy top-decile ETFs only if P \> MA( *T ′) Short bottom-decile ETFs only if P \< MA( *T ′) (362)

Here P is the ETF's price at the time of the transaction, and MA( *T ′) is computed using daily prices ( *T ′ can but need not be equal T; e.g., T ′ can be 100 to 200 days).

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.1.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: 4.1 plus the moving-average filter: long leg only if its price is above MA(200), short leg only if below MA(200).

Proxies and assumptions: Same sector ETFs; MA length 200 is my pick inside the paper's 100-200 range.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/4.1.1-sector-momentum-rotation-with-ma-filter/multi.json --out strategies/catalog/4.1.1-sector-momentum-rotation-with-ma-filter/multi.results.json`.

Compounded over the forward windows: strategy -2.5%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 2 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 126 | 0.00% | 0.00% | 3.82% | 0+0 |
| 2017-07-01..2018-01-01 | 252 | 2.36% | 0.00% | 5.35% | 4+3 |
| 2018-07-01..2019-01-01 | 252 | -1.13% | 0.00% | -2.98% | 5+5 |
| 2019-07-01..2020-01-01 | 126 | 0.56% | 0.00% | 4.57% | 7+8 |
| 2020-07-01..2021-01-01 | 126 | 3.64% | 0.00% | 10.57% | 4+4 |
| 2021-07-01..2022-01-01 | 126 | -2.47% | 0.00% | 5.50% | 3+4 |
| 2022-07-01..2023-01-01 | 252 | 2.73% | 0.00% | 1.21% | 3+2 |
| 2023-07-01..2024-01-01 | 126 | -2.95% | 0.00% | 3.80% | 8+8 |
| 2024-07-01..2025-01-01 | 252 | -2.14% | 0.00% | 3.87% | 6+8 |
| 2025-07-01..2026-01-01 | 252 | -2.84% | 0.00% | 5.47% | 9+8 |
