# 4.5 Leveraged ETFs (LETFs)

- Section: 4.5
- Asset class: Exchange-traded funds
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

A leveraged (inverse) ETF seeks to double or triple (the inverse of) the daily return of

its underlying index. 82 To maintain a daily leverage of 2 *× or 3 *×, LETFs rebalance

81 An equivalent but more symmetrical measure is Y = IBS − 1 */ 2 = ( *P C − P ∗) */ ( *P H − P L), where P ∗ = ( *P H + P L) */ 2. Note that Y ranges from 1 */ 2 for P C = P H to − 1 */ 2 for P C = P L.

every day, which requires buying on the days when the market is up and selling when the market is down. This can result in a negative drift in the long term, which can be exploited by shorting both a leveraged ETF and a leveraged inverse ETF (both with the same leverage and for the same underlying index) and investing the proceeds into, e.g., a Treasury ETF. This strategy can have a significant downside risk in the short term if one of the short ETF legs has a sizable positive return.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.5. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Short equal parts of a 3x S&P 500 ETF (SPXL) and a 3x inverse ETF (SPXS), proceeds in SHY; half size each because the runner caps gross at 2x.

Proxies and assumptions: The actual ETFs. Windows start later than 2016 because the shared history of the three ETFs is the limit.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/4.5-leveraged-etfs-letfs/multi.json --out strategies/catalog/4.5-leveraged-etfs-letfs/multi.results.json`.

Compounded over the forward windows: strategy 29.8%, buy-and-hold 11.4% (SPY), cash 0%; beat the benchmark in 5 of 8 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2017-12-01..2018-06-01 | 0 | -0.80% | 0.00% | 1.56% | 1+1 |
| 2018-12-01..2019-06-01 | 0 | 3.88% | 0.00% | -0.38% | 1+2 |
| 2019-12-01..2020-06-01 | 0 | 19.48% | 0.00% | -1.06% | 1+2 |
| 2020-12-01..2021-06-01 | 0 | -3.90% | 0.00% | 7.45% | 1+2 |
| 2021-12-01..2022-06-01 | 0 | 3.09% | 0.00% | -4.74% | 1+2 |
| 2022-12-01..2023-06-01 | 0 | 2.50% | 0.00% | 1.43% | 1+2 |
| 2023-12-01..2024-06-01 | 0 | -2.47% | 0.00% | 7.99% | 1+2 |
| 2024-12-01..2025-06-01 | 0 | 6.45% | 0.00% | -0.78% | 1+2 |
