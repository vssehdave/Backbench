# 5.3 Barbells

- Section: 5.3
- Asset class: Fixed income
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

In this strategy all purchased bonds are concentrated in two maturities T 1 (short maturity) and T 2 (long maturity), so this portfolio is a combination of two bullet strategies. This strategy takes advantage of the higher yields from the long-maturity bonds while hedging the interest rate risk with the short-maturity bonds: if the interest rates rise, the long-maturity bonds will lose value, but the proceeds from the short-maturity bonds can be reinvested at higher rates. 88 The modified duration (call it D) of the barbell strategy is the same as the modified duration (call it *D ∗) of a bullet strategy with a mid-range maturity (call it T ∗, T 1 \< T ∗ \< T 2 ). However, the convexity (call it C) of the barbell strategy is higher than the convexity (call it C ∗) of this bullet strategy. Intuitively this can be understood by noting that modified duration scales approximately linearly with maturity, while convexity scales approximately quadratically with maturity. For illustrative purposes and simplicity, let us consider a barbell strategy consisting of w 1 dollars' worth of zerocoupon bonds with short maturity T 1 and w 2 dollars' worth of zero-coupon bonds with long maturity T2 (each bond has $1 face value). Furthermore, let us assume continuous compounding and a constant yield Y. We then have $$ D = ew1 T1 + ew2 T2 $$ e *w 1 + e *w 2 (390)

T∗= D∗= D (391) $$ C = ew1 T 2 $$ 1 + e *w 2 T 2 e *w 1 + e *w 2 (392)

∗= T 2 *∗ (393)

where e *w 1 = w 1 exp( *− T 1 Y) and e *w 2 = w 2 exp( *− T 2 Y). Straightforward algebra gives

*C − C ∗ = e *w 1 e *w 2 ( ew1 + ew2)2 (T2 −T1)2 > 0 (394)

Higher convexity of the barbell portfolio provides a better protection against parallel shifts in the yield curve. However, this comes at the expense of a lower overall yield.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 5.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Barbell: equal capital in short (SHY) and long (TLT) Treasury ETFs, monthly.

Proxies and assumptions: SHY and TLT stand in for the two maturities.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/5.3-barbells/multi.json --out strategies/catalog/5.3-barbells/multi.results.json`.

Compounded over the forward windows: strategy -3.6%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 1 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 0 | -3.86% | 0.00% | 3.82% | 2+0 |
| 2017-07-01..2018-01-01 | 0 | 0.63% | 0.00% | 5.35% | 2+0 |
| 2018-07-01..2019-01-01 | 0 | 0.63% | 0.00% | -2.98% | 2+0 |
| 2019-07-01..2020-01-01 | 0 | 1.03% | 0.00% | 4.57% | 2+0 |
| 2020-07-01..2021-01-01 | 0 | -0.60% | 0.00% | 10.57% | 2+0 |
| 2021-07-01..2022-01-01 | 0 | 0.72% | 0.00% | 5.50% | 2+0 |
| 2022-07-01..2023-01-01 | 0 | -3.46% | 0.00% | 1.21% | 2+0 |
| 2023-07-01..2024-01-01 | 0 | 0.26% | 0.00% | 3.80% | 2+0 |
| 2024-07-01..2025-01-01 | 0 | 0.34% | 0.00% | 3.87% | 2+0 |
| 2025-07-01..2026-01-01 | 0 | 0.80% | 0.00% | 5.47% | 2+0 |
