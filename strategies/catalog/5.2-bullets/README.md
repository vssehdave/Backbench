# 5.2 Bullets

- Section: 5.2
- Asset class: Fixed income
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

In a bullet portfolio, all bonds have the same maturity date T thereby targeting a specific segment of the yield curve. The maturity can be picked based on the trader's outlook on the future interest rates: if the interest rates are expected to fall (i.e., the bond prices to rise), then picking a longer maturity would make more sense; if the interest rates are expected to rise (i.e., the bond prices to fall), then a shorter maturity would be more warranted; however, if the trader is uncertain about the future interest rates, a more diversified portfolio (e.g., a barbell/ladder portfolio - see below) is in order (as opposed to a bullet portfolio). Typically, the bonds in a bullet portfolio are purchased over time, which mitigates the interest rate risk to some extent: if the interest rates rise, the later bond purchases will be at higher rates; if the interest rates fall, the earlier bond purchases will have higher yields. 87

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Bullet: one maturity held, the 7-10 year Treasury ETF.

Proxies and assumptions: IEF stands in for a bond bullet.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/5.2-bullets/multi.json --out strategies/catalog/5.2-bullets/multi.results.json`.

Compounded over the forward windows: strategy -1.9%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 1 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 0 | -3.41% | 0.00% | 3.82% | 1+0 |
| 2017-07-01..2018-01-01 | 0 | 0.03% | 0.00% | 5.35% | 1+0 |
| 2018-07-01..2019-01-01 | 0 | 1.49% | 0.00% | -2.98% | 1+0 |
| 2019-07-01..2020-01-01 | 0 | 0.63% | 0.00% | 4.57% | 1+0 |
| 2020-07-01..2021-01-01 | 0 | -0.45% | 0.00% | 10.57% | 1+0 |
| 2021-07-01..2022-01-01 | 0 | 0.04% | 0.00% | 5.50% | 1+0 |
| 2022-07-01..2023-01-01 | 0 | -3.02% | 0.00% | 1.21% | 1+0 |
| 2023-07-01..2024-01-01 | 0 | 0.83% | 0.00% | 3.80% | 1+0 |
| 2024-07-01..2025-01-01 | 0 | 0.69% | 0.00% | 3.87% | 1+0 |
| 2025-07-01..2026-01-01 | 0 | 1.33% | 0.00% | 5.47% | 1+0 |
