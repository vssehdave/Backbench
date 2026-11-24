# 3.8 Pairs trading

- Section: 3.8
- Asset class: Stocks
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

*i, and shorting stocks in the bottom decile (with (non)uniform weights).

3.8

This dollar-neutral strategy amounts to identifying a pair of historically highly correlated stocks (call them stock A and stock B) and, when a mispricing (i.e., a deviation from the high historical correlation) occurs, shorting the "rich" stock and buying the "cheap" stock. This is an example of a mean-reversion strategy. Let P A ( *t 1 ) and *P B ( *t 1 ) be the prices of stock A and stock B at time t 1, and let P A ( *t 2 ) and P B ( *t 2 ) be the prices of stock A and stock B at a later time t 2. All prices are fully adjusted for any splits and dividends. The corresponding returns (from t 1 to t 2 ) are

RA = PA(t2) *P A ( *t 1 ) − 1 (283)

RB = PB(t2) *P B ( *t 1 ) − 1 (284)

Since typically these returns are small, we can use an alternative definition: *R A = ln  *P A ( *t 2 ) *P A ( *t 1 )  (285) *R B = ln  *P B ( *t 2 ) *P B ( *t 1 )  (286)

Next, let e *R A and e *R B be the demeaned returns:

R = 1

2 ( R A + R B ) (287)

e R A = R A − R (288) e *R B = R B − R (289)

where R is the mean return. A stock is "rich" if its demeaned return is positive, and it is "cheap" if its demeaned return is negative. The numbers of shares Q A, Q B to short/buy are fixed by the total desired dollar investment I (Eq. (290)) and the requirement of dollar-neutrality (Eq. (291)):

P A \| Q A \| + P B \| Q B \| = I (290) PA QA + PB QB = 0 (291)

where P A, P B are the stock prices at the time t ∗ the position is established ( *t ∗ ≥ t 2 ). 52

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 3.8. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Pairs trading, KO vs PEP: every month short the one with the higher 21-day return, buy the other, equal dollars. Long/short.

Proxies and assumptions: The pair KO/PEP is my assumption (a classic pair, not fitted); the paper gives no tickers. Benchmark SPY.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/3.8-pairs-trading/multi.json --out strategies/catalog/3.8-pairs-trading/multi.results.json`.

Compounded over the forward windows: strategy -7.9%, buy-and-hold 49.0% (SPY), cash 0%; beat the benchmark in 2 of 10 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2016-07-01..2017-01-01 | 21 | -0.98% | 0.00% | 3.82% | 5+5 |
| 2017-07-01..2018-01-01 | 21 | 1.29% | 0.00% | 5.35% | 4+4 |
| 2018-07-01..2019-01-01 | 21 | 1.00% | 0.00% | -2.98% | 5+5 |
| 2019-07-01..2020-01-01 | 21 | -2.27% | 0.00% | 4.57% | 3+3 |
| 2020-07-01..2021-01-01 | 21 | -3.10% | 0.00% | 10.57% | 3+3 |
| 2021-07-01..2022-01-01 | 21 | -1.95% | 0.00% | 5.50% | 1+1 |
| 2022-07-01..2023-01-01 | 21 | -3.19% | 0.00% | 1.21% | 3+3 |
| 2023-07-01..2024-01-01 | 21 | 1.15% | 0.00% | 3.80% | 4+4 |
| 2024-07-01..2025-01-01 | 21 | 4.07% | 0.00% | 3.87% | 4+4 |
| 2025-07-01..2026-01-01 | 21 | -3.87% | 0.00% | 5.47% | 3+3 |
