# 4.1 Sector momentum rotation

- Section: 4.1
- Asset class: Exchange-traded funds
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

Empirical evidence suggests that the momentum effect exists not only for individual stocks but also for sectors and industries. 74 A sector momentum rotation strategy is

based on overweighing holdings in outperforming sectors and underweighing holdings in underperforming sectors, where the "outperformance" and "underperformance" are based on momentum during the past T -month formation period (which typically ranges from 6 to 12 months). ETFs concentrated in specific sectors/industries offer a simple way to implement sector/industry rotation without having to buy or sell a large number of underlying stocks. Similarly to Subsection 3.1, as a measure of sector/industry momentum, we can use the corresponding ETF's cumulative return: *cum*

*i $$ (t) = $$ *P i ( *t) *P i ( *t + T) − 1 (361)

Here P i ( *t) is the price of the ETF labeled by i. (As above, t + T is T months in the *past w.r.t. t.) Right after time t, the trader can, e.g., buy the ETFs in the top decile by R cum*

*i ( *t) and hold the portfolio for a holding period (typically 1 to 3 months). Dollar-neutral strategies can also be constructed by, e.g., buying ETFs in the top decile and shorting ETFs in the bottom decile (as stocks, ETFs can be shorted). 75

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Sector rotation on nine sector ETFs: monthly, long the top performer and short the bottom over the lookback, half a unit each. Lookback 126 or 252 days chosen in the training window.

Proxies and assumptions: The nine Select Sector SPDR ETFs (XLB, XLE, XLF, XLI, XLK, XLP, XLU, XLV, XLY) stand in for the paper's stock universe; the top and bottom decile of nine is one ETF. XLC and XLRE are excluded (short history).

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/4.1-sector-momentum-rotation/multi.json --out strategies/catalog/4.1-sector-momentum-rotation/multi.results.json`.

Compounded over the forward windows: strategy -8.9%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 2 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 126 | 0.00% | 0.00% | 3.82% | 0+0 |
| 2017-07-01..2018-01-01 | 252 | 0.77% | 0.00% | 5.35% | 5+3 |
| 2018-07-01..2019-01-01 | 252 | -1.55% | 0.00% | -2.98% | 8+6 |
| 2019-07-01..2020-01-01 | 126 | 1.07% | 0.00% | 4.57% | 8+9 |
| 2020-07-01..2021-01-01 | 126 | 2.55% | 0.00% | 10.57% | 4+4 |
| 2021-07-01..2022-01-01 | 126 | -9.67% | 0.00% | 5.50% | 7+7 |
| 2022-07-01..2023-01-01 | 252 | 7.21% | 0.00% | 1.21% | 1+1 |
| 2023-07-01..2024-01-01 | 126 | -3.10% | 0.00% | 3.80% | 10+10 |
| 2024-07-01..2025-01-01 | 126 | -1.99% | 0.00% | 3.87% | 8+10 |
| 2025-07-01..2026-01-01 | 252 | -3.64% | 0.00% | 5.47% | 8+8 |
