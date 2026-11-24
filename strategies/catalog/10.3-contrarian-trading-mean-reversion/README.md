# 10.3 Contrarian trading (mean-reversion)

- Section: 10.3
- Asset class: Futures
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

This strategy is similar to the mean-reversion strategy discussed in Subsection 3.9. Within a given universe of futures labeled by i = 1 ,..., N, the "market index" return is calculated as an equally weighted average: $$ Rm = 1 $$

N

N X $$ i=1 $$

where R i are the individual futures returns (typically over the last one week). The capital allocation weights w i then are given by wi = −\gamma [Ri −Rm] (470)

where γ \> 0 is fixed via the normalization condition

N X $$ i=1 $$ |wi| = 1 (471)

Note that the strategy is automatically dollar-neutral. It amounts to buying losers and selling winners w.r.t. the market index (see, e.g., \[Wang and Yu, 2004\]). 168 As in the case of equities, the simple weighting scheme given by Eq. (470) is prone to overinvesting in volatile futures, which can be mitigated by suppressing w i by 1 */σ i or 1/\sigma2

*i, where σ i are the historical volatilities. The portfolio is rebalanced weekly.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 10.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Contrarian: weekly, weights proportional to (mean return - own return) over 5 days, gross 1, dollar-neutral, long/short.

Proxies and assumptions: The ETF basket from 4.6 stands in for futures.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/10.3-contrarian-trading-mean-reversion/multi.json --out strategies/catalog/10.3-contrarian-trading-mean-reversion/multi.results.json`.

Compounded over the forward windows: strategy -21.3%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 0 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 5 | -4.70% | 0.00% | 3.82% | 145+135 |
| 2017-07-01..2018-01-01 | 5 | -0.55% | 0.00% | 5.35% | 143+139 |
| 2018-07-01..2019-01-01 | 5 | -4.39% | 0.00% | -2.98% | 140+141 |
| 2019-07-01..2020-01-01 | 5 | -0.20% | 0.00% | 4.57% | 144+143 |
| 2020-07-01..2021-01-01 | 5 | -0.81% | 0.00% | 10.57% | 142+135 |
| 2021-07-01..2022-01-01 | 5 | -2.64% | 0.00% | 5.50% | 141+133 |
| 2022-07-01..2023-01-01 | 5 | -4.94% | 0.00% | 1.21% | 141+140 |
| 2023-07-01..2024-01-01 | 5 | -3.58% | 0.00% | 3.80% | 128+131 |
| 2024-07-01..2025-01-01 | 5 | -2.58% | 0.00% | 3.87% | 134+138 |
| 2025-07-01..2026-01-01 | 5 | 0.99% | 0.00% | 5.47% | 125+139 |
