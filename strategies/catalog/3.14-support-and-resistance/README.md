# 3.14 Support and resistance

- Section: 3.14
- Asset class: Stocks
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

This strategy uses "support" S and "resistance" R levels, which can be computed using the "pivot point" (a.k.a. the "center") C as follows: 56

C = PH + PL + PC (325)

R = 2 \times C −PL (326) S = 2 \times C −PH (327)

Here P H, P L and P C are the previous day's high, low and closing prices. One way to define a trading signal is as follows (as above, P is the current price): Signal =         

Establish long position if P \> C Liquidate long position if P ≥ R Establish short position if P \< C Liquidate short position if P ≤ S (328)

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.14. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Previous-bar pivot C=(H+L+C)/3, R=2C-L, S=2C-H (Eqs. 326-327); long when C<P<R, short when S<P<C, else flat; uses the last completed bar. Long/short, borrow 50 bps/yr. The paper's liquidate rules (P>=R, P<=S) are the flat zones.

Proxies and assumptions: SPY itself; no proxy.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/3.14-support-and-resistance/multi.json --out strategies/catalog/3.14-support-and-resistance/multi.results.json`.

Compounded over the forward windows: strategy -23.3%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 1 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 0 | -1.25% | 0.00% | 3.82% | 44+45 |
| 2017-07-01..2018-01-01 | 0 | -3.27% | 0.00% | 5.35% | 46+43 |
| 2018-07-01..2019-01-01 | 0 | 1.46% | 0.00% | -2.98% | 40+41 |
| 2019-07-01..2020-01-01 | 0 | -3.35% | 0.00% | 4.57% | 44+43 |
| 2020-07-01..2021-01-01 | 0 | -2.96% | 0.00% | 10.57% | 35+39 |
| 2021-07-01..2022-01-01 | 0 | -1.68% | 0.00% | 5.50% | 40+42 |
| 2022-07-01..2023-01-01 | 0 | -3.86% | 0.00% | 1.21% | 39+37 |
| 2023-07-01..2024-01-01 | 0 | -3.29% | 0.00% | 3.80% | 42+42 |
| 2024-07-01..2025-01-01 | 0 | -4.29% | 0.00% | 3.87% | 43+43 |
| 2025-07-01..2026-01-01 | 0 | -3.51% | 0.00% | 5.47% | 42+44 |

### Kraken BTC variant

Same rule on Kraken XBTUSD daily bars (UTC, 24/7, 26 bps fee). Kraken serves only the latest 720 days, so this is one 6-month forward window, not a 2016-2026 test: -13.7% vs B&H -6.9% (XBTUSD), cash 0%. Run `python catalog_run.py strategies/catalog/3.14-support-and-resistance/multi_btc.json --out strategies/catalog/3.14-support-and-resistance/multi_btc.results.json --start 2024-12-05 --end 2026-11-23`.

| Forward window | Selected | Strategy | Cash | Buy and hold (XBTUSD) | Fills |
|---|---|---|---|---|---|
| 2025-06-01..2025-12-01 | 0 | -13.66% | 0.00% | -6.95% | 63+63 |
