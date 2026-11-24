# 4.1.2 Dual-momentum sector rotation

- Section: 4.1.2
- Asset class: Exchange-traded funds
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

In long-only strategies, to mitigate the risk of buying ETFs when the broad market is trending down, relative (i.e., cross-sectional) momentum of sector ETFs can be augmented by the absolute (i.e., time-series) momentum of, e.g., a broad market index ETF (see, e.g., \[Antonacci, 2014\], \[Antonacci, 2017\]). 76 So, a long position based on the sector rotation signal (discussed above) is established only if the broad

market index has an upward trend; otherwise, the total available funds are invested into an ETF (e.g., gold or Treasury ETF) uncorrelated with the broad market index: Rule = (

Buy top-decile ETFs if P \> MA( *T ′) Buy an uncorrelated ETF if P ≤ MA( *T ′) (363)

Here P is the broad market index ETF's price at the time of the transaction, and MA( *T ′) is the moving average of this ETF's price. Typically, T ′ is 100 to 200 days.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.1.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Long-only absolute filter: hold the top sector ETF while SPY is above MA(200), else hold GLD.

Proxies and assumptions: Sector ETFs; GLD stands in for the paper's uncorrelated safe asset; SPY as the market index.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/4.1.2-dual-momentum-sector-rotation/multi.json --out strategies/catalog/4.1.2-dual-momentum-sector-rotation/multi.results.json`.

Compounded over the forward windows: strategy 12.2%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 1 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 126 | 0.00% | 0.00% | 3.82% | 0+0 |
| 2017-07-01..2018-01-01 | 252 | 8.06% | 0.00% | 5.35% | 3+2 |
| 2018-07-01..2019-01-01 | 252 | -3.17% | 0.00% | -2.98% | 4+3 |
| 2019-07-01..2020-01-01 | 126 | 2.32% | 0.00% | 4.57% | 5+4 |
| 2020-07-01..2021-01-01 | 126 | 9.95% | 0.00% | 10.57% | 3+2 |
| 2021-07-01..2022-01-01 | 126 | -1.81% | 0.00% | 5.50% | 2+1 |
| 2022-07-01..2023-01-01 | 252 | -1.32% | 0.00% | 1.21% | 2+1 |
| 2023-07-01..2024-01-01 | 126 | -0.37% | 0.00% | 3.80% | 4+3 |
| 2024-07-01..2025-01-01 | 252 | -1.98% | 0.00% | 3.87% | 5+4 |
| 2025-07-01..2026-01-01 | 252 | 0.69% | 0.00% | 5.47% | 4+3 |
