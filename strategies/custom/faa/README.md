# FAA, Flexible Asset Allocation (Keller and van Putten 2012)

Rules (paper's RAVC default, no tuning): rank 7 assets on relative momentum R (4-month return, high is good), volatility V
and average correlation C to the other six (both low is good; same 4-month window). Score = 1.0 x rank(R) + 0.5 x rank(V) +
0.5 x rank(C). Hold the top 3 at 1/3 each. A pick with R < 0 (absolute momentum filter) is replaced by cash. Monthly
rebalance, decided at the month-end close and filled next session. 4 months = 84 sessions; ties broken by universe order.

Data: Alpaca daily SIP bars (adjusted closes). Run: `python strategies/custom/faa/run.py` (writes `results.json`).
Manifest: `manifest.json` (xsection engine, entry `faa_rules:decide`).

ETF proxies for the paper's funds (not on Alpaca): VTI for VTSMX (US stocks), EFA for FDIVX (developed ex-US),
EEM for VEIEX (emerging), AGG for VBMFX (US bonds), DBC for QRAAX (commodities), VNQ for VGSIX (REITs),
SHY for VFISX (T-bills, also the cash asset). Cash earns SHY's return, not 0.

Caveats: data starts 2016-01, so the first decision is 2016-05-31 and the test is 10.4 years, much shorter than the paper's
and a period with no big stock/bond crash except 2020 and 2022. 5 bps slippage plus IBKR-like fees (see `results.json`).
ETFs are survivors by construction. Results are one path, not evidence of an edge.

| 2016-05-31 to 2026-10-30 | CAGR | Vol | Sharpe | Max DD | Turnover/yr | Costs/yr |
|---|---|---|---|---|---|---|
| FAA | 5.6% | 8.4% | 0.68 | -11.6% | 7.4x | 0.43% |
| SPY buy and hold | 14.9% | 17.5% | 0.88 | -33.8% | 0 | ~0 |
| Equal-weight 7 ETFs | 8.0% | 11.6% | 0.72 | -25.8% | | |
| Cash (0%) | 0 | 0 | | 0 | | |

Sharpe uses a 0% risk-free rate (as everywhere in this repo). FAA lowered drawdowns but lagged SPY badly.
