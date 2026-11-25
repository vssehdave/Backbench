# 4.1 Sector momentum rotation

- Section: 4.1
- Asset class: Exchange-traded funds
- Harness status: **tested**. Headline result: the cross-sectional harness (xs harness result). The multi-asset runner result is a stated variant (see below).

## Description (paper)

Empirical evidence suggests that the momentum effect exists not only for individual stocks but also for sectors and industries. 74 A sector momentum rotation strategy is

based on overweighing holdings in outperforming sectors and underweighing holdings in underperforming sectors, where the "outperformance" and "underperformance" are based on momentum during the past T -month formation period (which typically ranges from 6 to 12 months). ETFs concentrated in specific sectors/industries offer a simple way to implement sector/industry rotation without having to buy or sell a large number of underlying stocks. Similarly to Subsection 3.1, as a measure of sector/industry momentum, we can use the corresponding ETF's cumulative return: *cum*

*i $$ (t) = $$ *P i ( *t) *P i ( *t + T) − 1 (361)

Here P i ( *t) is the price of the ETF labeled by i. (As above, t + T is T months in the *past w.r.t. t.) Right after time t, the trader can, e.g., buy the ETFs in the top decile by R cum*

*i ( *t) and hold the portfolio for a holding period (typically 1 to 3 months). Dollar-neutral strategies can also be constructed by, e.g., buying ETFs in the top decile and shorting ETFs in the bottom decile (as stocks, ETFs can be shorted). 75

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 4.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Variant (multi-asset runner, not the headline)

Rule as implemented: Sector rotation on nine sector ETFs: monthly, long the top performer and short the bottom over the lookback, half a unit each. Lookback 126 or 252 days chosen in the training window.

Proxies and assumptions: The nine Select Sector SPDR ETFs (XLB, XLE, XLF, XLI, XLK, XLP, XLU, XLV, XLY) stand in for the paper's stock universe; the top and bottom decile of nine is one ETF. XLC and XLRE are excluded (short history).

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/4.1-sector-momentum-rotation/multi.json --out strategies/catalog/4.1-sector-momentum-rotation/multi.results.json`.

Compounded over the forward windows: strategy -10.4%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 2 of 10 windows. CAGR -2.14%, max drawdown -19.5%. Dollar-neutral (long the top ETF and short the bottom ETF, half of the start cash each) and half-invested; the headline is the long-only form the paper lists first.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 126 | 0.00% | 0.00% | 3.82% | 0+0 |
| 2017-07-01..2018-01-01 | 252 | 0.62% | 0.00% | 5.35% | 9+7 |
| 2018-07-01..2019-01-01 | 252 | -1.60% | 0.00% | -2.98% | 9+8 |
| 2019-07-01..2020-01-01 | 126 | 1.05% | 0.00% | 4.57% | 8+10 |
| 2020-07-01..2021-01-01 | 126 | 3.27% | 0.00% | 10.57% | 6+9 |
| 2021-07-01..2022-01-01 | 126 | -9.62% | 0.00% | 5.50% | 10+8 |
| 2022-07-01..2023-01-01 | 252 | 6.43% | 0.00% | 1.21% | 4+7 |
| 2023-07-01..2024-01-01 | 126 | -3.10% | 0.00% | 3.80% | 10+10 |
| 2024-07-01..2025-01-01 | 252 | -3.39% | 0.00% | 3.87% | 9+10 |
| 2025-07-01..2026-01-01 | 252 | -3.64% | 0.00% | 5.47% | 10+8 |

## xs harness result

Construction: Long the top-decile sector ETF (one of 11 SPDR ETFs) by 12-month return, monthly.
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: survivorship-biased; survivorship-biased: today's 11 SPDR sector ETFs, thin universe (one ETF held).

Summary over the 9 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | +9.6% | +8.0% | 1.12 |
| equal-weight | +7.3% | +7.2% | 1.38 |
| SPY | +8.8% | +10.9% | 1.52 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.25%, turnover 8.8x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +0.0% | +3.4% | +7.9% | +0.0% | n/a | 0.00% (no trades) |
| 2017-07-03..2017-12-29 | +16.5% | +9.9% | +11.5% | +0.0% | 2.93 | 0.33% |
| 2018-07-02..2018-12-31 | -8.1% | -7.6% | -6.9% | +0.0% | -0.72 | 0.28% |
| 2019-07-01..2019-12-31 | +17.7% | +8.8% | +10.9% | +0.0% | 3.01 | 0.42% |
| 2020-07-01..2020-12-31 | +24.7% | +20.0% | +22.1% | +0.0% | 1.89 | 0.05% |
| 2021-07-01..2021-12-31 | +8.0% | +10.5% | +11.7% | +0.0% | 0.81 | 0.18% |
| 2022-07-01..2022-12-30 | +23.0% | +3.9% | +2.3% | +0.0% | 1.38 | 0.05% |
| 2023-07-03..2023-12-29 | +5.0% | +6.1% | +8.0% | +0.0% | 0.65 | 0.27% |
| 2024-07-01..2024-12-31 | -0.4% | +7.2% | +8.4% | +0.0% | 0.04 | 0.39% |
| 2025-07-01..2025-12-31 | -0.1% | +6.8% | +11.0% | +0.0% | 0.07 | 0.28% |


## Reconciliation of the two runs

Both runs use the same ten July-December windows, the same Alpaca split- and dividend-adjusted bars and the same universe of sector ETFs (the xs run adds XLC and XLRE once they have history). Reduced to the same metric over those windows: xs +118.2% (CAGR 16.95%, max drawdown -20.6%); multi-asset as run (dollar-neutral, half capital) -10.4% (CAGR -2.14%, max drawdown -19.5%); the same multi-asset rule long-only at 252 days, full size: +90.9% (CAGR 13.69%, max drawdown -21.5%).

Why they differed (checked by changing one thing at a time on the same data):
- **Bug, fixed.** `python catalog_run.py ...` ran the module as `__main__`, so the rules' `Rebalance` was a different class from the one the runner tested for, and the monthly re-size never happened. The multi-asset results are regenerated with the fix (`test_catalog_multi.py` covers it).
- **Construction.** The multi-asset rule is dollar-neutral (long the top ETF, short the bottom ETF, half the start cash each) and earns nothing on the other half. The xs rule is long-only, fully invested. The paper's text says to buy the top decile and lists the dollar-neutral form second ("can also be constructed"), so the long-only form is the headline.
- **Cash limit.** The multi-asset runner sizes at the last close and fills at the next open, and rejects a buy when cash is short. At the full 10,000 that rejected 26 buys in 4.1.2 (20% total against 61% at 9,000 and 64% in the xs run), which is why the runner holds only half.
- **Conventions (small).** Fill at the next close with 5 bps slippage (xs) against the next open (multi-asset); one fixed 12-month lookback against 126 or 252 days chosen per fold; XLC and XLRE included from their first bar. A decile of nine or eleven ETFs is one ETF either way. Next-open fills would lift the 4.1 headline, so next-close is the more conservative choice.

Trusted result: the xs run, because it is the paper's primary form, fully invested, and its costs are charged on every fill. Whole-period SPY on the same windows is +125.2% (CAGR 17.69%, max drawdown -19.3%), so the mean-fold lead over equal-weight above does not mean the strategy beat SPY over the whole period.
