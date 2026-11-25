# Custom daily strategies

Each folder has a README (rules, data, proxies, caveats, results), a manifest, `results.json` and code. Shared helpers: `customlib.py`
and `edgar.py` at the repo root. Offline tests: `test_custom.py`.

| Folder | Idea | Engine | Period | CAGR vs SPY |
|---|---|---|---|---|
| `faa/` | Flexible Asset Allocation, 7 ETFs, top 3, monthly, every model in the paper | `xsection.py` | 2016-06 to 2026-10 | 4.9% (default RAVC) vs 14.9% |
| `sp500-top-holding/` | 100% in the largest S&P 500 company by EDGAR-based market cap | `xsection.py` | 2016-01 to 2026-10 | 15.0% vs 14.7% |
| `momentum-60d/` | Long when 60-day return is positive, else cash (SPY, QQQ, BTC) | `harness.py` | 2016 to 2025 (BTC 2 years) | SPY 9.5% vs 12.7%, QQQ 11.5% vs 18.6% |
| `munger-200wma/` | Quality stocks at or below the 200-week MA, exit 20% above | `xsection.py` | 2019-10 to 2026-10 | 12.5% vs 15.6% |

## Standard report, headline run of each strategy

From each run's `report.json` (one continuous backtest, rf = 0, beta and alpha vs SPY, 252 sessions a year; MC DD p95 is the
95th-percentile max drawdown of the Monte Carlo paths). Every variant has its own REPORT.md, equity.svg and best, worst and random
day trades under its `results/` folder.

| Strategy | CAGR | Sharpe | Sortino | beta | alpha | maxDD | MC DD p95 | link |
|---|---|---|---|---|---|---|---|---|
| `faa/` (default RAVC) | 5.0% | 0.61 | 0.83 | 0.26 | +1.2% | -10.9% | 33.7% | [REPORT](faa/results/ladder_ravc/REPORT.md) |
| `momentum-60d/` SPY | 9.7% | 0.93 | 1.26 | 0.37 | +4.8% | -18.9% | 35.5% | [REPORT](momentum-60d/results/SPY/REPORT.md) |
| `momentum-60d/` QQQ | 11.7% | 0.84 | 1.15 | 0.46 | +5.7% | -17.8% | 43.1% | [REPORT](momentum-60d/results/QQQ/REPORT.md) |
| `momentum-60d/` BTC | 4.0% | 0.29 | 0.44 | 0.16 | +5.4% | -28.7% | 52.8% | [REPORT](momentum-60d/results/BTC/REPORT.md) |
| `sp500-top-holding/` | not yet run | | | | | | | |
| `munger-200wma/` | not yet run | | | | | | | |
| `../intraday/orb/` long-short 2 bps | -22.8% | -0.14 | -0.22 | 0.05 | -9.1% | -90.2% | 99.4% | [REPORT](../intraday/orb/results/long_short_2bps/REPORT.md) |
| `../intraday/orb-top50/` 5-min long-short | -43.2% | -12.14 | -10.08 | 0.00 | -56.4% | -97.9% | 99.1% | [REPORT](../intraday/orb-top50/5min-long-short/results/REPORT.md) |
| `../intraday/overnight/` SPY 2 bps | -2.4% | -0.16 | -0.21 | 0.42 | -7.8% | -37.8% | 67.8% | [REPORT](../intraday/overnight/results/SPY_overnight_2bps/REPORT.md) |

None beat buy and hold on return; all have survivorship or data limits stated in their READMEs.
