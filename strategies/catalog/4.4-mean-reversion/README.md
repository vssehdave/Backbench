# 4.4 Mean-reversion

- Section: 4.4
- Asset class: Exchange-traded funds
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

One way (among myriad others) to construct a mean-reversion strategy for ETFs is

to use the Internal Bar Strength (IBS) based on the previous day's close P C, high *P H and low P L prices: 80

IBS = P C − P L

P H − P L

(370)

Note that IBS ranges from 0 to 1. 81 An ETF can be thought of as being "rich" if its

IBS is close to 1, and as "cheap" if its IBS is close to 0. Upon sorting a universe of ETFs cross-sectionally by IBS, a dollar-neutral strategy can, e.g., be constructed by selling ETFs in the top decile and buying ETFs in the bottom decile. As with stock strategies discussed above, weights can be uniform for all long and all short ETFs, respectively, or nonuniform, e.g., based on historical ETF volatilities. Furthermore, mean-reversion strategies we discussed above for stocks can also be adapted to ETFs.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.4. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Internal bar strength IBS=(C-L)/(H-L) of the previous daily bar on the nine sector ETFs: buy the lowest, short the highest, one unit each. Long/short.

Proxies and assumptions: Sector ETFs stand in for the paper's stock universe (top/bottom decile of nine is one name). Uses daily high/low only.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/4.4-mean-reversion/multi.json --out strategies/catalog/4.4-mean-reversion/multi.results.json`.

Compounded over the forward windows: strategy -38.5%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 1 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 0 | -1.29% | 0.00% | 3.82% | 207+210 |
| 2017-07-01..2018-01-01 | 0 | -11.57% | 0.00% | 5.35% | 219+198 |
| 2018-07-01..2019-01-01 | 0 | 4.04% | 0.00% | -2.98% | 217+207 |
| 2019-07-01..2020-01-01 | 0 | -6.59% | 0.00% | 4.57% | 232+218 |
| 2020-07-01..2021-01-01 | 0 | 3.93% | 0.00% | 10.57% | 222+205 |
| 2021-07-01..2022-01-01 | 0 | 0.84% | 0.00% | 5.50% | 219+197 |
| 2022-07-01..2023-01-01 | 0 | -3.81% | 0.00% | 1.21% | 219+203 |
| 2023-07-01..2024-01-01 | 0 | -12.91% | 0.00% | 3.80% | 217+207 |
| 2024-07-01..2025-01-01 | 0 | -17.69% | 0.00% | 3.87% | 231+214 |
| 2025-07-01..2026-01-01 | 0 | 0.38% | 0.00% | 5.47% | 222+215 |
