# 3.1 Price-momentum

- Section: 3.1
- Asset class: Stocks
- Harness status: **tested: cross-sectional harness** (`python money.py xs strategies/catalog/3.1-price-momentum/xs_manifest.json`; results in `xs_results.json`) - **survivorship-biased**; see labels below.

## Description (paper)

Empirically, there appears to be certain "inertia" in stock returns known as the momentum effect, whereby future returns are positively correlated with past returns (see, e.g., \[Asness, 1994\], \[Asness et al, 2014\], \[Asness, Moskowitz and Pedersen, 2013\], \[Grinblatt and Moskowitz, 2004\], \[Jegadeesh and Titman, 1993\]). Let t denote time measured in the units of 1 month, with t = 0 corresponding to the most recent time. Let P i ( *t) be the time series of prices (fully adjusted for splits and dividends) for the stock labeled by i ( *i = 1 ,..., N, where N is the number of stocks in the trading universe). Let

$$ Ri(t) = $$ *P i ( *t) *P i ( *t + 1) − 1 (266) *cum*

*i $$ = $$ *P i ( *S) *P i ( *S + T) − 1 (267) *mean i $$ = 1 $$

T

S + T − 1 X t=S *R i ( *t) (268) *risk.adj i = R mean i i (269) $$ i = $$ *T − 1

S + T − 1 X t=S ( *R i ( *t) − R mean i) 2 (270)

Here: R i ( *t) is the monthly return; R cum*

*i is the cumulative return computed over the *T -month "formation period" (usually T = 12) skipping the most recent S -month "skip period" (usually S = 1); 35 R mean*

*i is the risk-adjusted mean return over the formation period; and σ i is the monthly volatility calculated over the formation period.

The price-momentum strategy amounts to buying the best performing stocks and selling the worst performing stocks, where the "performance" is measured by a selection criterion based on R cum i, R mean i, R risk.adj*

*i (in the decreasing order), the trader can, e.g., buy stocks in the top decile (winners) and short stocks in the bottom decile (losers). 36

This can be a zero-cost strategy, i.e., the corresponding portfolio is dollar-neutral. Alternatively, a long-only portfolio can be constructed by buying stocks in, e.g., the top decile. Once a portfolio is established at t = 0, it is kept unaltered during

a predefined "holding period", 37 which can be 1 month or longer (longer holding period portfolios typically have diminishing returns before trading costs as the momentum effect fades with time). Multi-month-holding portfolios can be constructed by overlapping 1-month-holding portfolios (see, e.g., \[Jegadeesh and Titman, 1993\]).

The above prescription does not fix the relative weights w i of the stocks in the portfolio. For a long-only portfolio we have w i ≥ 0 and

N X $$ i=1 $$ $$ wi = 1 $$ (271)

So, if the total investment level is I, then the stock labeled by i has I × w i dollars invested in it. This, up to rounding, translates into Q i = I × w i /P i (0) shares. 38 One can simply take uniform weights, w i = 1 */N for all stocks, albeit other weighting schemes are possible. E.g., we can have nonuniform w i ∝ 1 */σ i, or w i ∝ 1 */σ 2

*i, etc. For a dollar-neutral portfolio we can have negative w i and

N X $$ i=1 $$ |wi| = 1 (272)

N X $$ i=1 $$ $$ wi = 0 $$ (273)

So, if the total investment level is I = I L + *I S, where I L is the total long investment, and I S is the absolute value of the total short investment, 39 then the stock labeled by i has I × w i dollars invested in it, where w i \> 0 for long stocks, and w i \< 0 for short stocks. One can simply take modulus-uniform weights, where w i = 1 */ 2 *N L for all N L long stocks, and w i = − 1 */ 2 *N S for all N S short stocks. However, other weighting schemes are possible, e.g., as above, weights suppressed by σ i, σ 2 *i, etc. 40

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.1. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## xs harness result

Construction: Long the top decile and short the bottom decile of the S&P 500 by cumulative return over 12 months skipping the latest month (R_cum, eq. 267), equal weights, dollar neutral.
Parameters are the paper's defaults, no tuning. Monthly rebalance, walk-forward folds (July-December windows 2016-2025), costs and borrow from `xsection.py`. Reproduce all with `python strategies/xs/run_catalog.py`.

Labels: survivorship-biased; survivorship-biased S&P 500 universe.

Summary over the 9 of 10 folds that traded (the rest abstained for lack of history); benchmarks use the same folds. Six-month returns.

| | mean | median | mean Sharpe |
|---|---|---|---|
| strategy | -1.2% | +0.1% | -0.02 |
| equal-weight | +8.0% | +7.6% | 1.24 |
| SPY | +8.8% | +10.9% | 1.52 |
| cash | +0.0% | +0.0% | n/a |

Mean cost drag per fold 0.37%, turnover 8.0x per year.

| test window | strategy | equal-weight | SPY | cash | Sharpe | cost drag |
|---|---|---|---|---|---|---|
| 2016-07-01..2016-12-30 | +0.0% | +8.8% | +7.9% | +0.0% | n/a | 0.00% (no trades) |
| 2017-07-03..2017-12-29 | +0.1% | +9.9% | +11.5% | +0.0% | 0.07 | 0.39% |
| 2018-07-02..2018-12-31 | +1.7% | -9.1% | -6.9% | +0.0% | 0.45 | 0.37% |
| 2019-07-01..2019-12-31 | -4.1% | +8.2% | +10.9% | +0.0% | -0.62 | 0.37% |
| 2020-07-01..2020-12-31 | -13.1% | +26.7% | +22.1% | +0.0% | -0.84 | 0.37% |
| 2021-07-01..2021-12-31 | -2.7% | +8.6% | +11.7% | +0.0% | -0.46 | 0.38% |
| 2022-07-01..2022-12-30 | +3.5% | +6.3% | +2.3% | +0.0% | 0.53 | 0.34% |
| 2023-07-03..2023-12-29 | -3.7% | +6.4% | +8.0% | +0.0% | -0.73 | 0.36% |
| 2024-07-01..2024-12-31 | +1.8% | +7.6% | +8.4% | +0.0% | 0.45 | 0.37% |
| 2025-07-01..2025-12-31 | +5.3% | +7.2% | +11.0% | +0.0% | 0.97 | 0.39% |
