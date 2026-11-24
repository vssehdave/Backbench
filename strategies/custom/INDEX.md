# Custom daily strategies

Each folder has a README (rules, data, proxies, caveats, results), a manifest, `results.json` and code. Shared helpers: `customlib.py`
and `edgar.py` at the repo root. Offline tests: `test_custom.py`.

| Folder | Idea | Engine | Period | CAGR vs SPY |
|---|---|---|---|---|
| `faa/` | Flexible Asset Allocation, 7 ETFs, top 3, monthly | `xsection.py` | 2016-06 to 2026-10 | 5.6% vs 14.9% |
| `sp500-top-holding/` | 100% in the largest S&P 500 company by EDGAR-based market cap | `xsection.py` | 2016-01 to 2026-10 | 13.4% vs 14.7% |
| `momentum-60d/` | Long when 60-day return is positive, else cash (SPY, QQQ, BTC) | `harness.py` | 2016 to 2025 (BTC 2 years) | SPY 9.5% vs 12.7%, QQQ 11.5% vs 18.6% |
| `munger-200wma/` | Quality stocks at or below the 200-week MA, exit 20% above | `xsection.py` | 2019-10 to 2026-10 | 12.5% vs 15.6% |

None beat buy and hold on return; all have survivorship or data limits stated in their READMEs.
