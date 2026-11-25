# intraday-orb-top50

## Range x side x slippage (monthly point-in-time top 50, notional capped at equity / 50)

| config | CAGR | Sharpe | max DD | trades | win rate | avg trade bps | max position % equity |
|---|---|---|---|---|---|---|---|
| 5min long-only 0bps | -32.7% | -7.82 | -93.5% | 49477 | 31.5% | -33.3 | 2.0 |
| 5min long-only 2bps | -37.2% | -9.70 | -96.0% | 42657 | 28.5% | -45.6 | 2.0 |
| 5min long-only 5bps | -39.5% | -10.80 | -96.8% | 35788 | 25.8% | -58.2 | 2.0 |
| 5min long-short 0bps | -41.8% | -11.76 | -97.6% | 45785 | 29.0% | -49.2 | 2.0 |
| 5min long-short 2bps | -43.1% | -12.14 | -97.9% | 40094 | 27.4% | -59.0 | 2.0 |
| 5min long-short 5bps | -44.0% | -12.59 | -98.2% | 34115 | 24.9% | -71.4 | 2.0 |
| 10min long-only 0bps | -27.9% | -6.24 | -89.5% | 49344 | 34.6% | -27.3 | 2.0 |
| 10min long-only 2bps | -34.7% | -8.68 | -94.7% | 43084 | 30.4% | -41.3 | 2.0 |
| 10min long-only 5bps | -38.3% | -10.41 | -96.4% | 36059 | 27.2% | -55.2 | 2.0 |
| 10min long-short 0bps | -41.6% | -11.45 | -97.5% | 45764 | 30.5% | -49.1 | 2.0 |
| 10min long-short 2bps | -42.9% | -11.79 | -97.9% | 39988 | 28.5% | -58.9 | 2.0 |
| 10min long-short 5bps | -44.0% | -12.33 | -98.1% | 34018 | 25.8% | -71.3 | 2.0 |
| 15min long-only 0bps | -24.7% | -5.39 | -85.8% | 47994 | 36.3% | -24.1 | 2.0 |
| 15min long-only 2bps | -32.7% | -8.06 | -93.5% | 42627 | 31.5% | -38.4 | 2.0 |
| 15min long-only 5bps | -37.4% | -10.17 | -96.0% | 35881 | 27.6% | -54.1 | 2.0 |
| 15min long-short 0bps | -41.2% | -11.22 | -97.4% | 46582 | 31.3% | -47.3 | 2.0 |
| 15min long-short 2bps | -42.5% | -11.47 | -97.8% | 40599 | 29.3% | -57.1 | 2.0 |
| 15min long-short 5bps | -43.8% | -12.15 | -98.1% | 34631 | 26.4% | -69.7 | 2.0 |
| SPY buy and hold | 13.1% | 0.72 | -33.8% | | | | |

## Sensitivity: notional capped at equity / 10 instead of / 50 (2 bps)

| config | CAGR | Sharpe | max DD | trades | avg trade bps |
|---|---|---|---|---|---|
| 5min long-only 2bps | -32.0% | -2.76 | -93.1% | 30329 | -25.2 |
| 5min long-short 2bps | -49.4% | -5.96 | -99.1% | 29668 | -39.4 |
| 10min long-only 2bps | -26.0% | -2.23 | -88.6% | 27396 | -24.0 |
| 10min long-short 2bps | -41.4% | -4.62 | -97.5% | 29022 | -35.5 |
| 15min long-only 2bps | -22.8% | -1.89 | -84.8% | 25679 | -21.9 |
| 15min long-short 2bps | -37.1% | -4.14 | -95.9% | 28053 | -33.2 |

## Old 5-minute config (monthly top 20 by dollar volume from the 103 candidates), sizing cap off vs on

| config | cap | CAGR | Sharpe | max DD | trades | max position % equity |
|---|---|---|---|---|---|---|
| 5min long-only 0bps cap none | none | -4.8% | 0.24 | -74.5% | 12163 | 400 |
| 5min long-only 2bps cap none | none | -67.3% | -1.49 | -100.0% | 10503 | 399 |
| 5min long-only 5bps cap none | none | -74.1% | -2.47 | -100.0% | 5370 | 351 |
| 5min long-short 0bps cap none | none | 38.4% | 0.83 | -68.2% | 12679 | 400 |
| 5min long-short 2bps cap none | none | -22.7% | -0.14 | -90.2% | 12863 | 400 |
| 5min long-short 5bps cap none | none | -73.8% | -2.48 | -100.0% | 6646 | 382 |
| 5min long-only 0bps cap equity/20 | equity/20 | -3.5% | -0.36 | -24.6% | 24398 | 5 |
| 5min long-only 2bps cap equity/20 | equity/20 | -12.3% | -1.48 | -60.1% | 24398 | 5 |
| 5min long-only 5bps cap equity/20 | equity/20 | -26.5% | -3.66 | -88.1% | 24016 | 5 |
| 5min long-short 0bps cap equity/20 | equity/20 | -8.3% | -0.96 | -49.8% | 34313 | 5 |
| 5min long-short 2bps cap equity/20 | equity/20 | -27.0% | -3.75 | -89.0% | 33541 | 5 |
| 5min long-short 5bps cap equity/20 | equity/20 | -43.4% | -7.70 | -98.1% | 25622 | 5 |

## 5-minute range, long-short, 2 bps: per stock (fixed $10,000 per trade, 100+ trades, top and bottom 10 by total P&L)

| symbol | trades | total P&L USD | mean bps/trade | win rate | profit factor |
|---|---|---|---|---|---|
| TSLA | 1475 | 22,206 | 15.3 | 44.2% | 1.20 |
| NVDA | 1727 | 4,379 | 2.5 | 41.5% | 1.04 |
| ORCL | 1663 | 4,104 | 2.5 | 42.1% | 1.05 |
| AVGO | 1711 | 3,167 | 2.0 | 40.6% | 1.03 |
| KLAC | 169 | 2,785 | 17.5 | 45.0% | 1.22 |
| PANW | 117 | 2,698 | 23.4 | 52.1% | 1.30 |
| MU | 287 | 2,631 | 9.8 | 44.3% | 1.09 |
| AMD | 1057 | 2,603 | 2.4 | 40.6% | 1.03 |
| APP | 104 | 1,745 | 17.7 | 43.3% | 1.17 |
| AMT | 166 | 1,014 | 6.1 | 44.6% | 1.14 |
| ... | | | | | |
| LIN | 1627 | -13,435 | -8.4 | 34.4% | 0.77 |
| HD | 1714 | -13,584 | -8.1 | 40.3% | 0.81 |
| MRK | 1596 | -13,686 | -8.6 | 39.0% | 0.80 |
| CVX | 1706 | -14,189 | -8.4 | 39.6% | 0.81 |
| PG | 1632 | -15,271 | -9.4 | 37.9% | 0.72 |
| PEP | 1599 | -15,504 | -9.8 | 37.5% | 0.74 |
| BAC | 1713 | -16,856 | -9.9 | 39.8% | 0.80 |
| KO | 1723 | -17,558 | -10.2 | 36.5% | 0.71 |
| JNJ | 1710 | -20,349 | -12.0 | 37.0% | 0.67 |
| ABBV | 1572 | -21,891 | -14.0 | 37.2% | 0.69 |

Winners (top 20% of 78 stocks by total P&L, 2020-2026) vs the rest: median of per-stock mean feature, and Spearman rho of stock P&L vs the feature across all of them. Winners: TSLA, NVDA, ORCL, AVGO, KLAC, PANW, MU, AMD, APP, AMT, LRCX, SBUX, NOW, ISRG, DELL, AMAT

| feature | winners median | rest median | rho with stock P&L |
|---|---|---|---|
| range_pct | 0.01431 | 0.008163 | 0.69 |
| atr_pct | 0.04535 | 0.02455 | 0.72 |
| gap_abs | 0.01327 | 0.007091 | 0.65 |
| dollar_volume | 2.614e+09 | 1.199e+09 | 0.28 |
| beta | 2.012 | 0.8829 | 0.70 |
| price | 391.1 | 179 | 0.32 |
| cap_rank | 34.45 | 31.88 | 0.29 |

Sectors (winners / rest): Communication Services 1/6; Consumer Discretionary 2/4; Consumer Staples 0/6; Energy 0/2; Financials 0/8; Health Care 1/13; Industrials 0/9; Information Technology 11/12; Materials 0/1; Real Estate 1/0; Utilities 0/1

Winners (top 20% of 62 stocks by total P&L, 2020-2022 only) vs the rest: median of per-stock mean feature, and Spearman rho of stock P&L vs the feature across all of them. Winners: TSLA, AMD, INTU, MRNA, LLY, COP, AMT, NVDA, SBUX, AMZN, AAPL, CVS

| feature | winners median | rest median | rho with stock P&L |
|---|---|---|---|
| range_pct | 0.009649 | 0.008109 | 0.40 |
| atr_pct | 0.03158 | 0.0252 | 0.50 |
| gap_abs | 0.009346 | 0.007512 | 0.40 |
| dollar_volume | 3.718e+09 | 1.133e+09 | 0.03 |
| beta | 1.116 | 0.8989 | 0.37 |
| price | 237 | 138.1 | 0.23 |
| cap_rank | 41.5 | 27.64 | 0.31 |

Sectors (winners / rest): Communication Services 0/6; Consumer Discretionary 3/3; Consumer Staples 0/6; Energy 1/1; Financials 0/6; Health Care 3/11; Industrials 0/5; Information Technology 4/10; Materials 0/1; Real Estate 1/0; Utilities 0/1

Features vs per-trade return, all trades pooled (Spearman rho; mean bps of lowest and highest quintile; first half 2020-2022 and second half 2023-2026 bottom/top bps).

| feature | n | rho | bottom bps | top bps | top-bottom | first half rho | second half rho |
|---|---|---|---|---|---|---|---|
| range_pct | 83774 | -0.104 | -6.3 | -3.1 | 3.2 | -0.145 | -0.075 |
| atr_pct | 83774 | -0.113 | -6.8 | -2.1 | 4.8 | -0.144 | -0.086 |
| gap_abs | 83774 | -0.065 | -6.7 | -4.3 | 2.4 | -0.081 | -0.051 |
| dollar_volume | 83774 | -0.046 | -7.3 | 0.0 | 7.4 | -0.050 | -0.050 |
| beta | 83774 | -0.059 | -7.8 | 0.4 | 8.3 | -0.051 | -0.063 |
| price | 83774 | -0.007 | -7.6 | -3.1 | 4.6 | -0.003 | -0.015 |
| cap_rank | 83774 | 0.003 | -2.5 | -5.3 | -2.8 | 0.006 | -0.000 |

Sector (today's S&P membership; stocks since removed are 'unknown'): Communication Services 9061 trades -5.5 bps; Consumer Discretionary 6988 trades -1.4 bps; Consumer Staples 10012 trades -7.5 bps; Energy 2099 trades -7.4 bps; Financials 8948 trades -7.0 bps; Health Care 16151 trades -8.3 bps; Industrials 4952 trades -7.8 bps; Information Technology 22674 trades -2.3 bps; Materials 1627 trades -8.4 bps; Real Estate 166 trades 6.1 bps; Utilities 1096 trades -5.9 bps

Stock picks: top 20% by mean bps in 2020-2022 (12 of 62 stocks with 60+ trades): 10.8 bps in sample, -1.9 bps in 2023-2026 (7422 trades, P&L -13,860 USD) versus -5.5 for the other stocks and -4.5 for all. Rank correlation of per-stock mean, first vs second half: 0.23 over 54 stocks.

Chance (200 within-day shuffles of returns across stocks): stocks with t > 2 observed 1 vs 0.1 expected (95th pct 1) of 85 stocks with 50+ trades (binomial with independent stocks: 1.9 expected, P(at least observed) = 0.86); largest t 2.64 vs 1.46 (95th pct 2.23); second-half bps of first-half picks -1.9 vs -4.5 (95th pct -2.0, p = 0.04).

Feature rules, tercile cut points from 2020-2022 only:

| feature | rule | 2020-2022 bps (n) | 2023-2026 bps (n) | 2023-2026 naive t |
|---|---|---|---|---|
| range_pct | top tercile | -8.8 (12272) | -1.7 (18229) | -1.4 |
| range_pct | bottom tercile | -5.7 (12271) | -6.6 (14199) | -11.1 |
| atr_pct | top tercile | -7.6 (12272) | 0.8 (13573) | 0.5 |
| atr_pct | bottom tercile | -5.4 (12271) | -6.4 (17919) | -10.8 |
| gap_abs | top tercile | -8.0 (12272) | -0.9 (13891) | -0.7 |
| gap_abs | bottom tercile | -7.3 (12271) | -5.7 (17338) | -7.8 |
| dollar_volume | top tercile | -4.0 (12288) | -1.7 (20595) | -1.6 |
| dollar_volume | bottom tercile | -7.0 (12252) | -7.5 (10273) | -8.8 |
| beta | top tercile | -3.7 (12272) | -1.7 (17852) | -1.4 |
| beta | bottom tercile | -8.9 (12271) | -6.7 (18945) | -10.2 |
| price | top tercile | -3.3 (12272) | -3.6 (20845) | -4.0 |
| price | bottom tercile | -8.6 (12271) | -5.0 (9648) | -4.5 |
| cap_rank | top tercile | -5.5 (12494) | -5.5 (15755) | -5.5 |
| cap_rank | bottom tercile | -5.5 (11904) | -3.3 (15363) | -3.1 |

## 10-minute range, long-short, 2 bps: per stock (fixed $10,000 per trade, 100+ trades, top and bottom 10 by total P&L)

| symbol | trades | total P&L USD | mean bps/trade | win rate | profit factor |
|---|---|---|---|---|---|
| TSLA | 1465 | 19,330 | 13.5 | 46.7% | 1.17 |
| PANW | 115 | 1,851 | 16.4 | 51.3% | 1.23 |
| AMT | 164 | 1,557 | 9.5 | 47.0% | 1.21 |
| APP | 100 | 1,435 | 14.5 | 41.0% | 1.15 |
| KLAC | 169 | 1,277 | 7.2 | 42.6% | 1.10 |
| NVDA | 1713 | 1,137 | 0.6 | 45.1% | 1.01 |
| NOW | 382 | 1,005 | 2.8 | 47.4% | 1.06 |
| GE | 724 | 883 | 1.2 | 44.8% | 1.03 |
| SBUX | 105 | 423 | 4.0 | 47.6% | 1.13 |
| ISRG | 257 | 230 | 0.8 | 44.4% | 1.02 |
| ... | | | | | |
| MCD | 1577 | -12,527 | -8.0 | 40.7% | 0.77 |
| CSCO | 1698 | -12,934 | -7.6 | 41.7% | 0.81 |
| CVX | 1689 | -13,156 | -7.9 | 42.1% | 0.82 |
| PEP | 1582 | -13,285 | -8.5 | 39.8% | 0.77 |
| AMGN | 1003 | -14,519 | -14.6 | 39.7% | 0.70 |
| KO | 1706 | -15,487 | -9.1 | 38.5% | 0.73 |
| BAC | 1690 | -17,468 | -10.4 | 42.3% | 0.79 |
| MRK | 1574 | -17,627 | -11.3 | 40.0% | 0.75 |
| ABBV | 1555 | -19,331 | -12.5 | 40.8% | 0.72 |
| JNJ | 1686 | -19,878 | -11.9 | 39.6% | 0.67 |

Winners (top 20% of 78 stocks by total P&L, 2020-2026) vs the rest: median of per-stock mean feature, and Spearman rho of stock P&L vs the feature across all of them. Winners: TSLA, PANW, AMT, APP, KLAC, NVDA, NOW, GE, SBUX, ISRG, MU, DELL, QCOM, PLTR, COP, ORCL

| feature | winners median | rest median | rho with stock P&L |
|---|---|---|---|
| range_pct | 0.01356 | 0.009899 | 0.63 |
| atr_pct | 0.0368 | 0.02456 | 0.67 |
| gap_abs | 0.01132 | 0.007202 | 0.61 |
| dollar_volume | 1.954e+09 | 1.239e+09 | 0.22 |
| beta | 1.488 | 0.8861 | 0.68 |
| price | 329.9 | 194.1 | 0.30 |
| cap_rank | 37.76 | 31.73 | 0.33 |

Sectors (winners / rest): Communication Services 1/6; Consumer Discretionary 2/4; Consumer Staples 0/6; Energy 1/1; Financials 0/8; Health Care 1/13; Industrials 1/8; Information Technology 9/14; Materials 0/1; Real Estate 1/0; Utilities 0/1

Winners (top 20% of 62 stocks by total P&L, 2020-2022 only) vs the rest: median of per-stock mean feature, and Spearman rho of stock P&L vs the feature across all of them. Winners: TSLA, AAPL, AMD, MRNA, AMZN, COP, INTU, AMT, SBUX, LLY, INTC, QCOM

| feature | winners median | rest median | rho with stock P&L |
|---|---|---|---|
| range_pct | 0.01168 | 0.009721 | 0.34 |
| atr_pct | 0.03164 | 0.02504 | 0.45 |
| gap_abs | 0.009436 | 0.007314 | 0.38 |
| dollar_volume | 1.651e+09 | 1.087e+09 | 0.01 |
| beta | 1.165 | 0.8827 | 0.34 |
| price | 206.4 | 138.3 | 0.30 |
| cap_rank | 39.98 | 27.68 | 0.29 |

Sectors (winners / rest): Communication Services 0/6; Consumer Discretionary 3/3; Consumer Staples 0/6; Energy 1/1; Financials 0/6; Health Care 2/12; Industrials 0/5; Information Technology 5/9; Materials 0/1; Real Estate 1/0; Utilities 0/1

Features vs per-trade return, all trades pooled (Spearman rho; mean bps of lowest and highest quintile; first half 2020-2022 and second half 2023-2026 bottom/top bps).

| feature | n | rho | bottom bps | top bps | top-bottom | first half rho | second half rho |
|---|---|---|---|---|---|---|---|
| range_pct | 82321 | -0.059 | -5.5 | -5.4 | 0.1 | -0.085 | -0.040 |
| atr_pct | 82321 | -0.072 | -6.7 | -3.3 | 3.4 | -0.093 | -0.054 |
| gap_abs | 82321 | -0.041 | -6.7 | -5.1 | 1.6 | -0.047 | -0.035 |
| dollar_volume | 82321 | -0.025 | -7.4 | -1.2 | 6.2 | -0.030 | -0.026 |
| beta | 82321 | -0.036 | -8.1 | -1.7 | 6.4 | -0.030 | -0.039 |
| price | 82321 | -0.005 | -7.7 | -4.1 | 3.6 | -0.001 | -0.011 |
| cap_rank | 82321 | 0.001 | -3.0 | -5.2 | -2.2 | 0.005 | -0.003 |

Sector (today's S&P membership; stocks since removed are 'unknown'): Communication Services 8944 trades -5.9 bps; Consumer Discretionary 6917 trades -1.5 bps; Consumer Staples 9885 trades -6.5 bps; Energy 2081 trades -6.5 bps; Financials 8815 trades -6.8 bps; Health Care 15739 trades -9.7 bps; Industrials 4858 trades -7.4 bps; Information Technology 22289 trades -3.2 bps; Materials 1544 trades -6.1 bps; Real Estate 164 trades 9.5 bps; Utilities 1085 trades -3.9 bps

Stock picks: top 20% by mean bps in 2020-2022 (12 of 62 stocks with 60+ trades): 11.4 bps in sample, -5.3 bps in 2023-2026 (6469 trades, P&L -33,601 USD) versus -5.6 for the other stocks and -5.2 for all. Rank correlation of per-stock mean, first vs second half: 0.14 over 54 stocks.

Chance (200 within-day shuffles of returns across stocks): stocks with t > 2 observed 1 vs 0.1 expected (95th pct 1) of 85 stocks with 50+ trades (binomial with independent stocks: 1.9 expected, P(at least observed) = 0.86); largest t 2.33 vs 1.44 (95th pct 2.24); second-half bps of first-half picks -5.3 vs -5.3 (95th pct -3.1, p = 0.49).

Feature rules, tercile cut points from 2020-2022 only:

| feature | rule | 2020-2022 bps (n) | 2023-2026 bps (n) | 2023-2026 naive t |
|---|---|---|---|---|
| range_pct | top tercile | -9.0 (12094) | -3.8 (17179) | -3.0 |
| range_pct | bottom tercile | -4.5 (12093) | -5.3 (14517) | -8.8 |
| atr_pct | top tercile | -7.0 (12094) | -1.2 (13406) | -0.8 |
| atr_pct | bottom tercile | -5.6 (12093) | -6.2 (17496) | -10.4 |
| gap_abs | top tercile | -6.8 (12094) | -3.5 (13700) | -2.5 |
| gap_abs | bottom tercile | -7.3 (12093) | -5.4 (16943) | -7.4 |
| dollar_volume | top tercile | -3.5 (12112) | -3.2 (20283) | -3.0 |
| dollar_volume | bottom tercile | -6.6 (12088) | -7.8 (10036) | -9.2 |
| beta | top tercile | -4.3 (12094) | -2.8 (17485) | -2.3 |
| beta | bottom tercile | -8.2 (12093) | -7.2 (18608) | -11.0 |
| price | top tercile | -3.5 (12095) | -5.1 (20336) | -5.5 |
| price | bottom tercile | -8.6 (12093) | -4.9 (9512) | -4.5 |
| cap_rank | top tercile | -5.7 (12286) | -5.4 (15341) | -5.4 |
| cap_rank | bottom tercile | -5.7 (11771) | -4.3 (15181) | -4.2 |

## 15-minute range, long-short, 2 bps: per stock (fixed $10,000 per trade, 100+ trades, top and bottom 10 by total P&L)

| symbol | trades | total P&L USD | mean bps/trade | win rate | profit factor |
|---|---|---|---|---|---|
| TSLA | 1455 | 13,546 | 9.6 | 47.2% | 1.12 |
| PANW | 106 | 2,961 | 28.4 | 54.7% | 1.45 |
| NVDA | 1701 | 2,937 | 1.6 | 47.3% | 1.03 |
| AMT | 158 | 2,353 | 15.2 | 48.1% | 1.37 |
| GE | 712 | 1,748 | 2.5 | 45.8% | 1.05 |
| MU | 276 | 1,281 | 4.8 | 46.0% | 1.05 |
| KLAC | 161 | 1,248 | 6.9 | 44.1% | 1.10 |
| PLTR | 454 | 1,202 | 2.6 | 44.9% | 1.03 |
| QCOM | 1241 | 894 | 0.7 | 45.1% | 1.01 |
| ISRG | 233 | 608 | 2.6 | 46.8% | 1.06 |
| ... | | | | | |
| CSCO | 1675 | -13,627 | -8.2 | 42.7% | 0.80 |
| AMGN | 967 | -13,841 | -14.5 | 40.0% | 0.70 |
| PEP | 1552 | -13,979 | -9.1 | 40.9% | 0.74 |
| KO | 1687 | -14,243 | -8.5 | 39.5% | 0.74 |
| CVX | 1670 | -14,932 | -9.0 | 42.6% | 0.80 |
| UNH | 1651 | -15,059 | -9.3 | 42.5% | 0.80 |
| BAC | 1675 | -15,480 | -9.3 | 43.9% | 0.80 |
| JNJ | 1662 | -17,501 | -10.6 | 40.7% | 0.69 |
| MRK | 1546 | -18,741 | -12.2 | 40.2% | 0.72 |
| ABBV | 1535 | -18,857 | -12.4 | 42.3% | 0.71 |

Winners (top 20% of 77 stocks by total P&L, 2020-2026) vs the rest: median of per-stock mean feature, and Spearman rho of stock P&L vs the feature across all of them. Winners: TSLA, PANW, NVDA, AMT, GE, MU, KLAC, PLTR, QCOM, ISRG, SBUX, NOW, DELL, ORCL, ANET

| feature | winners median | rest median | rho with stock P&L |
|---|---|---|---|
| range_pct | 0.01705 | 0.01087 | 0.60 |
| atr_pct | 0.04117 | 0.02457 | 0.65 |
| gap_abs | 0.01312 | 0.00713 | 0.60 |
| dollar_volume | 1.824e+09 | 1.238e+09 | 0.20 |
| beta | 1.55 | 0.8834 | 0.67 |
| price | 313.8 | 194.4 | 0.24 |
| cap_rank | 36.24 | 31.8 | 0.31 |

Sectors (winners / rest): Communication Services 0/6; Consumer Discretionary 2/4; Consumer Staples 0/6; Energy 0/2; Financials 0/8; Health Care 1/13; Industrials 1/8; Information Technology 10/13; Materials 0/1; Real Estate 1/0; Utilities 0/1

Winners (top 20% of 62 stocks by total P&L, 2020-2022 only) vs the rest: median of per-stock mean feature, and Spearman rho of stock P&L vs the feature across all of them. Winners: TSLA, AAPL, AMZN, AMD, AMT, INTU, COP, MRNA, INTC, SBUX, QCOM, AVGO

| feature | winners median | rest median | rho with stock P&L |
|---|---|---|---|
| range_pct | 0.01318 | 0.01075 | 0.26 |
| atr_pct | 0.03178 | 0.02504 | 0.37 |
| gap_abs | 0.009676 | 0.007178 | 0.32 |
| dollar_volume | 1.652e+09 | 1.033e+09 | 0.01 |
| beta | 1.238 | 0.8801 | 0.31 |
| price | 216.4 | 138.2 | 0.25 |
| cap_rank | 39.98 | 26.97 | 0.22 |

Sectors (winners / rest): Communication Services 0/6; Consumer Discretionary 3/3; Consumer Staples 0/6; Energy 1/1; Financials 0/6; Health Care 1/13; Industrials 0/5; Information Technology 6/8; Materials 0/1; Real Estate 1/0; Utilities 0/1

Features vs per-trade return, all trades pooled (Spearman rho; mean bps of lowest and highest quintile; first half 2020-2022 and second half 2023-2026 bottom/top bps).

| feature | n | rho | bottom bps | top bps | top-bottom | first half rho | second half rho |
|---|---|---|---|---|---|---|---|
| range_pct | 80814 | -0.036 | -5.2 | -4.7 | 0.5 | -0.056 | -0.022 |
| atr_pct | 80814 | -0.049 | -6.3 | -2.6 | 3.7 | -0.066 | -0.035 |
| gap_abs | 80814 | -0.026 | -6.2 | -3.9 | 2.3 | -0.031 | -0.020 |
| dollar_volume | 80814 | -0.015 | -7.1 | -1.5 | 5.6 | -0.020 | -0.015 |
| beta | 80814 | -0.020 | -8.0 | -1.1 | 6.9 | -0.016 | -0.022 |
| price | 80814 | -0.003 | -6.8 | -5.0 | 1.8 | -0.002 | -0.008 |
| cap_rank | 80814 | -0.001 | -3.3 | -4.8 | -1.5 | 0.001 | -0.002 |

Sector (today's S&P membership; stocks since removed are 'unknown'): Communication Services 8801 trades -6.2 bps; Consumer Discretionary 6849 trades -1.4 bps; Consumer Staples 9720 trades -6.0 bps; Energy 2060 trades -8.3 bps; Financials 8687 trades -5.9 bps; Health Care 15351 trades -10.3 bps; Industrials 4764 trades -7.3 bps; Information Technology 21895 trades -2.6 bps; Materials 1458 trades -4.8 bps; Real Estate 158 trades 15.2 bps; Utilities 1071 trades -2.8 bps

Stock picks: top 20% by mean bps in 2020-2022 (12 of 62 stocks with 60+ trades): 8.7 bps in sample, -3.5 bps in 2023-2026 (6422 trades, P&L -22,513 USD) versus -5.6 for the other stocks and -4.8 for all. Rank correlation of per-stock mean, first vs second half: 0.22 over 54 stocks.

Chance (200 within-day shuffles of returns across stocks): stocks with t > 2 observed 0 vs 0.1 expected (95th pct 1) of 85 stocks with 50+ trades (binomial with independent stocks: 1.9 expected, P(at least observed) = 1.00); largest t 1.93 vs 1.49 (95th pct 2.14); second-half bps of first-half picks -3.5 vs -4.9 (95th pct -2.8, p = 0.14).

Feature rules, tercile cut points from 2020-2022 only:

| feature | rule | 2020-2022 bps (n) | 2023-2026 bps (n) | 2023-2026 naive t |
|---|---|---|---|---|
| range_pct | top tercile | -8.2 (11919) | -3.1 (16364) | -2.4 |
| range_pct | bottom tercile | -5.2 (11918) | -4.8 (14502) | -8.1 |
| atr_pct | top tercile | -6.6 (11919) | -0.6 (13098) | -0.4 |
| atr_pct | bottom tercile | -5.8 (11918) | -5.9 (17168) | -10.0 |
| gap_abs | top tercile | -6.3 (11919) | -2.8 (13346) | -2.0 |
| gap_abs | bottom tercile | -7.0 (11918) | -5.2 (16638) | -7.2 |
| dollar_volume | top tercile | -3.9 (11935) | -3.1 (19816) | -3.0 |
| dollar_volume | bottom tercile | -6.1 (11918) | -7.5 (9769) | -8.9 |
| beta | top tercile | -3.7 (11919) | -2.3 (17063) | -2.0 |
| beta | bottom tercile | -8.4 (11918) | -7.3 (18250) | -11.4 |
| price | top tercile | -4.4 (11919) | -4.8 (19818) | -5.3 |
| price | bottom tercile | -7.9 (11917) | -4.1 (9358) | -3.7 |
| cap_rank | top tercile | -5.8 (12091) | -4.9 (14915) | -4.9 |
| cap_rank | bottom tercile | -4.7 (11629) | -4.4 (14968) | -4.3 |

Each run has its own folder next to this one (5min-long-short, ..., old-5min-top20-capped) with its README, results/REPORT.md, report.json and 2 bps trade logs. Full numbers are in ../results.json. No Monte Carlo section: that module lives on the unmerged research/monte-carlo branch.
