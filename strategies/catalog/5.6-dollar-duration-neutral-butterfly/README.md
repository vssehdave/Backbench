# 5.6 Dollar-duration-neutral butterfly

- Section: 5.6
- Asset class: Fixed income
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

This is a zero-cost combination of a long barbell portfolio (with short T 1 and long *T 3 maturities) and a short bullet portfolio (with a medium maturity T 2, where *T 1 \< T 2 \< T 3 ). Let: the dollar amounts invested in the 3 bonds be P 1 , P 2 , P 3; and

91 For the sake of simplicity, in Eq. (396) the number n = T ∗ /δ of compounding periods is assumed to be a whole number. Extension to non-integer T ∗ /δ is straightforward.

the corresponding modified durations be D 1 , D 2 , D 3. Then zero cost (i.e., dollarneutrality) and the dollar-duration-neutrality (the latter protects the portfolio from parallel shifts in the yield curve) imply that

P1 + P3 = P2 (404) $$ P1 D1 + P3 D3 = P2 D2 $$ (405)

This fixes P 1 , P 3 via P 2. While the portfolio is immune to parallel shifts in the yield curve, it is not immune to changes in the slope or the curvature of the yield curve. 93

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.6. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Dollar-duration-neutral butterfly: long SHY and TLT, short IEF, dollar-neutral and dollar-duration-neutral (Eqs. 404-405). Long/short.

Proxies and assumptions: Assumed modified durations 1.9 / 7.4 / 17.5 for SHY / IEF / TLT. ETF prices include coupon distributions.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/5.6-dollar-duration-neutral-butterfly/multi.json --out strategies/catalog/5.6-dollar-duration-neutral-butterfly/multi.results.json`.

Compounded over the forward windows: strategy -1.0%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 1 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 0 | 0.43% | 0.00% | 3.82% | 2+1 |
| 2017-07-01..2018-01-01 | 0 | 0.24% | 0.00% | 5.35% | 2+1 |
| 2018-07-01..2019-01-01 | 0 | -0.99% | 0.00% | -2.98% | 2+1 |
| 2019-07-01..2020-01-01 | 0 | 0.08% | 0.00% | 4.57% | 2+1 |
| 2020-07-01..2021-01-01 | 0 | -0.12% | 0.00% | 10.57% | 2+1 |
| 2021-07-01..2022-01-01 | 0 | 0.23% | 0.00% | 5.50% | 2+1 |
| 2022-07-01..2023-01-01 | 0 | 0.21% | 0.00% | 1.21% | 2+1 |
| 2023-07-01..2024-01-01 | 0 | -0.30% | 0.00% | 3.80% | 2+1 |
| 2024-07-01..2025-01-01 | 0 | -0.18% | 0.00% | 3.87% | 2+1 |
| 2025-07-01..2026-01-01 | 0 | -0.59% | 0.00% | 5.47% | 2+1 |
