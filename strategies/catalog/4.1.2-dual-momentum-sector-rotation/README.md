# 4.1.2 Dual-momentum sector rotation

- Section: 4.1.2
- Asset class: Exchange-traded funds
- Harness status: **tested**. Headline result: the cross-sectional harness (xs harness result). The multi-asset runner result is a stated variant (see below).

## Description (paper)

In long-only strategies, to mitigate the risk of buying ETFs when the broad market is trending down, relative (i.e., cross-sectional) momentum of sector ETFs can be augmented by the absolute (i.e., time-series) momentum of, e.g., a broad market index ETF (see, e.g., \[Antonacci, 2014\], \[Antonacci, 2017\]). 76 So, a long position based on the sector rotation signal (discussed above) is established only if the broad

market index has an upward trend; otherwise, the total available funds are invested into an ETF (e.g., gold or Treasury ETF) uncorrelated with the broad market index: Rule = (

Buy top-decile ETFs if P \> MA( *T ′) Buy an uncorrelated ETF if P ≤ MA( *T ′) (363)

Here P is the broad market index ETF's price at the time of the transaction, and MA( *T ′) is the moving average of this ETF's price. Typically, T ′ is 100 to 200 days.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.1.2. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Variant (multi-asset runner, not the headline)

Rule as implemented: Long-only absolute filter: hold the top sector ETF while SPY is above MA(200), else hold GLD.

Proxies and assumptions: Sector ETFs; GLD stands in for the paper's uncorrelated safe asset; SPY as the market index.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/4.1.2-dual-momentum-sector-rotation/multi.json --out strategies/catalog/4.1.2-dual-momentum-sector-rotation/multi.results.json`.

Compounded over the forward windows: strategy 12.9%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 1 of 10 windows. CAGR 2.44%, max drawdown -10.6%. Half-invested (5,000 of 10,000 in the position, cash earns 0) and the lookback is chosen per fold from 126 or 252 days; the headline holds the full amount at 252 days.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 126 | 0.00% | 0.00% | 3.82% | 0+0 |
| 2017-07-01..2018-01-01 | 252 | 7.93% | 0.00% | 5.35% | 4+5 |
| 2018-07-01..2019-01-01 | 252 | -3.29% | 0.00% | -2.98% | 4+5 |
| 2019-07-01..2020-01-01 | 126 | 2.30% | 0.00% | 4.57% | 6+5 |
| 2020-07-01..2021-01-01 | 126 | 10.46% | 0.00% | 10.57% | 4+4 |
| 2021-07-01..2022-01-01 | 126 | -1.83% | 0.00% | 5.50% | 4+4 |
| 2022-07-01..2023-01-01 | 252 | -1.16% | 0.00% | 1.21% | 5+1 |
| 2023-07-01..2024-01-01 | 126 | -0.32% | 0.00% | 3.80% | 4+4 |
| 2024-07-01..2025-01-01 | 252 | -1.76% | 0.00% | 3.87% | 5+6 |
| 2025-07-01..2026-01-01 | 252 | 0.76% | 0.00% | 5.47% | 5+5 |

## xs harness result

Construction: As 4.1 while SPY is above its 200-day average, otherwise GLD.
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: safe asset chosen: GLD; survivorship-biased; survivorship-biased: today's 11 SPDR sector ETFs, thin universe (one ETF held).

Summary over the 9 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | +6.2% | +3.1% | 0.87 |
| equal-weight | +7.4% | +8.7% | 1.51 |
| SPY | +8.8% | +10.9% | 1.52 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.29%, turnover 10.1x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +0.0% | +1.9% | +7.9% | +0.0% | n/a | 0.00% (no trades) |
| 2017-07-03..2017-12-29 | +16.5% | +9.5% | +11.5% | +0.0% | 2.93 | 0.33% |
| 2018-07-02..2018-12-31 | -10.4% | -6.8% | -6.9% | +0.0% | -1.1 | 0.39% |
| 2019-07-01..2019-12-31 | +17.7% | +8.7% | +10.9% | +0.0% | 3.01 | 0.42% |
| 2020-07-01..2020-12-31 | +24.7% | +18.8% | +22.1% | +0.0% | 1.89 | 0.05% |
| 2021-07-01..2021-12-31 | +8.0% | +9.9% | +11.7% | +0.0% | 0.81 | 0.18% |
| 2022-07-01..2022-12-30 | -3.2% | +3.6% | +2.3% | +0.0% | -0.26 | 0.16% |
| 2023-07-03..2023-12-29 | +3.1% | +6.2% | +8.0% | +0.0% | 0.44 | 0.37% |
| 2024-07-01..2024-12-31 | -0.4% | +7.7% | +8.4% | +0.0% | 0.04 | 0.39% |
| 2025-07-01..2025-12-31 | -0.1% | +8.7% | +11.0% | +0.0% | 0.07 | 0.28% |


## Reconciliation of the two runs

Both runs use the same ten July-December windows, the same Alpaca split- and dividend-adjusted bars and the same universe of sector ETFs (the xs run adds XLC and XLRE once they have history). Reduced to the same metric over those windows: xs +64.4% (CAGR 10.49%, max drawdown -22.6%); multi-asset as run (half capital, 126 or 252 days) +12.9% (CAGR 2.44%, max drawdown -10.6%). Both hold GLD when SPY is below its MA(200); cutting the multi-asset size to 9,000 so no buy is rejected gives +61.1% (CAGR 9.91%, max drawdown -18.4%).

Why they differed (checked by changing one thing at a time on the same data):
- **Bug, fixed.** `python catalog_run.py ...` ran the module as `__main__`, so the rules' `Rebalance` was a different class from the one the runner tested for, and the monthly re-size never happened. The multi-asset results are regenerated with the fix (`test_catalog_multi.py` covers it).
- **Construction.** The multi-asset rule is dollar-neutral (long the top ETF, short the bottom ETF, half the start cash each) and earns nothing on the other half. The xs rule is long-only, fully invested. The paper's text says to buy the top decile and lists the dollar-neutral form second ("can also be constructed"), so the long-only form is the headline.
- **Cash limit.** The multi-asset runner sizes at the last close and fills at the next open, and rejects a buy when cash is short. At the full 10,000 that rejected 26 buys in 4.1.2 (20% total against 61% at 9,000 and 64% in the xs run), which is why the runner holds only half.
- **Conventions (small).** Fill at the next close with 5 bps slippage (xs) against the next open (multi-asset); one fixed 12-month lookback against 126 or 252 days chosen per fold; XLC and XLRE included from their first bar. A decile of nine or eleven ETFs is one ETF either way. Next-open fills would lift the 4.1 headline, so next-close is the more conservative choice.

Trusted result: the xs run, because it is the paper's primary form, fully invested, and its costs are charged on every fill. Whole-period SPY on the same windows is +125.2% (CAGR 17.69%, max drawdown -19.3%), so the mean-fold lead over equal-weight above does not mean the strategy beat SPY over the whole period.
