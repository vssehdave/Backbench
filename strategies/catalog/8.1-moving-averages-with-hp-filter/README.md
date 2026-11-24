# 8.1 Moving averages with HP filter

- Section: 8.1
- Asset class: Foreign exchange
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

In Subsection 3.12 we discussed a trading strategy for stocks wherein the trading signal is based on 2 intersecting (shorter and longer) moving averages. A similar approach can be applied to FX as well. However, FX spot rate time series tend to be rather noisy, which can lead to false signals based on moving averages. To mitigate this, before computing the moving averages, the higher-frequency noise can first be filtered out, e.g., using the so-called Hodrick-Prescott (HP) filter. 140 Then, the remaining lower-frequency trend component (as opposed to the raw spot rate) can be used to compute the moving averages and generate the trading signal (see, e.g., \[Harris and Yilmaz, 2009\]). The HP filter is given by: $$ S(t) = S∗(t) + \nu(t) $$ (437) $$ g = $$

T X $$ t=1 $$ [S(t) −S∗(t)]2 + λ

T − 1 X $$ t=2 $$

\[ *S ∗ ( *t + 1) − 2 *S ∗ ( *t) + S ∗ ( *t − 1)\] 2 (438) *g → min (439)

Here: the objective function g is minimized w.r.t. the set of T values of S ∗ ( *t), t = 1 ,..., T; S ( *t) is the FX spot rate at time t; S ∗ ( *t) is the lower-frequency ("regular") component; ν ( *t) is the higher-frequency ("irregular") component, which is treated as noise; the first term in Eq. (438) minimizes the noise, while the second term (based on the discretized second derivative of S ∗ ( *t)) penalizes the variation in S ∗ ( *t); and λ is the smoothing parameter. There is no "fundamental" method to fix λ. Sometimes (but not always) it is set to λ = 100 *× n 2, where n is the data frequency measured on

an annual basis (see, e.g., \[Baxter and King, 1999\] for more detail). So, for monthly data, which is what is usually used in this context, n = 12. The estimation period usually spans several years (of monthly data). Once S ∗ ( *t) is determined, two moving averages MA( *T 1 ) and MA( *T 2 ), T 1 \< T 2, are calculated based on S ∗ ( *t). Then, as before, MA( *T 1 ) \> MA( *T 2 ) is a buy signal, and MA( *T 1 ) \< MA( *T 2 ) is a sell signal.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 8.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: HP-filtered FX trend: Hodrick-Prescott filter (lambda=100*252^2) of the last 252 days of log price, MA(10) vs MA(30) of the trend; long if the short MA is above, short if below. Long/short.

Proxies and assumptions: FXE (euro ETF) stands in for EUR/USD; benchmark FXE. ETF prices include distributions.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/8.1-moving-averages-with-hp-filter/multi.json --out strategies/catalog/8.1-moving-averages-with-hp-filter/multi.results.json`.

Compounded over the forward windows: strategy 5.8%, buy-and-hold 0.5% (FXE), cash 0%; beat the benchmark in 5 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (FXE) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 0 | 0.00% | 0.00% | -3.00% | 0+0 |
| 2017-07-01..2018-01-01 | 0 | 2.53% | 0.00% | 2.53% | 1+0 |
| 2018-07-01..2019-01-01 | 0 | 0.73% | 0.00% | -0.87% | 0+1 |
| 2019-07-01..2020-01-01 | 0 | 0.64% | 0.00% | -0.78% | 0+1 |
| 2020-07-01..2021-01-01 | 0 | 4.09% | 0.00% | 4.09% | 1+0 |
| 2021-07-01..2022-01-01 | 0 | 2.18% | 0.00% | -2.32% | 0+1 |
| 2022-07-01..2023-01-01 | 0 | -0.98% | 0.00% | 1.33% | 1+1 |
| 2023-07-01..2024-01-01 | 0 | -3.66% | 0.00% | 1.12% | 2+1 |
| 2024-07-01..2025-01-01 | 0 | 0.33% | 0.00% | -1.37% | 1+1 |
| 2025-07-01..2026-01-01 | 0 | -0.06% | 0.00% | -0.06% | 1+0 |
