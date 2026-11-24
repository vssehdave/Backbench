# 7.3 Volatility carry with two ETNs

- Section: 7.3
- Asset class: Volatility
- Harness status: **tested** (multi-asset runner, ETF proxies; see Results)

## Description (paper)

VXX is an exchange-traded note (ETN) that tracks VIX via a portfolio of shortmaturity (months 1 and 2) VIX futures contracts. To maintain a constant maturity, at the close of each day, a portion of the shorter-maturity futures is sold and replaced with the longer-maturity futures bought with the proceeds. Since the VIX futures curve is in contango most of the time, the longer-maturity futures are priced higher than the shorter-maturity futures, so this rebalancing amounts to a decay in the value of VXX over time, which is known as the roll (or contango) loss. Further, as time passes, the futures converge to the spot (VIX), so VXX loses value so long as the VIX futures curve is in contango. VXZ is yet another ETN that tracks VIX via a portfolio of medium-maturity (months 4 through 7) VIX futures. VXZ also suffers roll loss, but to a lesser degree than VXX as the slope of the VIX futures curve in contango decreases with maturity. 130 The basic strategy then is to short VXX and buy VXZ with the hedge ratio that can be determined via a serial regression. 131

This strategy is not without risks, however. There can be short-term spikes in VXX (the corresponding spikes in VXZ usually are sizably smaller), which can lead to substantial short-term P&L drawdowns, even if the strategy is overall profitable.

## Source

Kakushadze, Z. and Serur, J.A. (2018) *151 Trading Strategies*, SSRN 3247865, Section 7.3. The text above is that section only, lightly cleaned (ligatures fixed, most footnotes dropped); formulas are as extracted and may be garbled, so check the paper.

## Results (multi-asset runner)

Rule as implemented: Short VXX, long VXZ with the hedge ratio from a regression of VXX on VXZ daily returns over the last 60 days (clipped to 0-1), monthly. Long/short.

Proxies and assumptions: VXX and VXZ are the real ETNs, adjusted. Borrow cost is a flat 50 bps/yr; the real VXX borrow fee is higher, so this flatters the strategy.

Data: Alpaca daily SIP bars, split and dividend adjusted, via `catalog_data.py`. The runner `catalog_run.py` uses the same walk-forward, fee, fill and borrow rules as the single-instrument harness, over several symbols. Parameters are the paper's or the stated assumptions, no tuning. Run `python catalog_run.py strategies/catalog/7.3-volatility-carry-with-two-etns/multi.json --out strategies/catalog/7.3-volatility-carry-with-two-etns/multi.results.json`.

Compounded over the forward windows: strategy 62.2%, buy-and-hold 20.0% (SPY), cash 0%; beat the benchmark in 5 of 7 windows.

| Forward window | Selected | Strategy | Cash | Buy and hold (SPY) | Fills |
|---|---|---|---|---|---|
| 2018-08-01..2019-02-01 | 60 | -9.95% | 0.00% | -1.59% | 6+3 |
| 2019-08-01..2020-02-01 | 60 | 13.53% | 0.00% | 4.40% | 1+1 |
| 2020-08-01..2021-02-01 | 60 | 13.29% | 0.00% | 6.59% | 1+1 |
| 2021-08-01..2022-02-01 | 60 | 12.03% | 0.00% | 1.40% | 1+1 |
| 2022-08-01..2023-02-01 | 60 | 11.66% | 0.00% | 0.09% | 1+1 |
| 2023-08-01..2024-02-01 | 60 | 9.80% | 0.00% | 3.19% | 1+1 |
| 2024-08-01..2025-02-01 | 60 | 1.92% | 0.00% | 4.65% | 1+1 |
