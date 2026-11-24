# FAA, Flexible Asset Allocation (Keller and van Putten 2012)

Every model the paper reports, in its order, on ETF proxies. Default rules (RAVC, no tuning): rank 7 assets on relative
momentum R (4-month return, high is good), volatility V and average correlation C to the other six (both low is good,
daily returns over the same 4 months). Score = 1.0 x rank(R) + 0.5 x rank(V) + 0.5 x rank(C). Hold the top 3 at 1/3
each. A pick with R < 0 (absolute momentum, A) is replaced by cash. Decided at the month-end close, filled at the next
session's close. Ties broken by universe order. The paper's ladder switches factors on one at a time (`LADDER` in `run.py`).

Data: Alpaca daily SIP bars (adjusted closes). Run: `python strategies/custom/faa/run.py` (writes `results.json`, all
variants, decision logs for the ladder). Manifest: `manifest.json` (xsection engine, entry `faa_rules:decide`).

ETF proxies for the paper's funds (not on Alpaca): VTI for VTSMX (US stocks), EFA for FDIVX (developed ex-US),
EEM for VEIEX (emerging), AGG for VBMFX (US bonds), DBC for QRAAX (commodities), VNQ for VGSIX (REITs),
SHY for VFISX (T-bills, also the cash asset). Cash earns SHY's return, not 0. The paper itself suggests VEA/VWO/BND/GSG.

## Results, 2016-05-31 to 2026-10-30

Ours: 5 bps slippage plus IBKR-like fees, except the levered row, which uses the paper's tc 0.1% per trade and 3% a year
on the borrowed half. Paper columns are R / V / D / Sharpe(S0) / T as printed. n/r = the paper does not report it.

| Variant | CAGR | Vol | Sharpe | Max DD | Turnover/yr | Cost/yr | Paper 2005-12 (in-sample) | Paper 1998-2004 (out-of-sample) |
|---|---|---|---|---|---|---|---|---|
| Benchmark: equal weight 7, monthly rebalance | 7.7% | 10.7% | 0.75 | -24.5% | 0.3x | 0.04% | 5.6 / 16.6 / -46.3 / 0.34 / 0.1 | 8.3 / 9.8 / -15.2 / 0.85 / 0.1 |
| R only (top 3, no cash rule) | 9.4% | 12.1% | 0.81 | -19.5% | 5.8x | 0.34% | 9.1 / 14.5 / -29.2 / 0.63 / 2.9 | n/r |
| R + A | 8.6% | 11.2% | 0.80 | -19.6% | 5.8x | 0.34% | 11.7 / 12.8 / -12.6 / 0.92 / 2.9 | n/r |
| R, A, V 100/50/0 | 7.2% | 10.5% | 0.71 | -10.9% | 7.1x | 0.41% | 12.5 / 11.7 / -11.4 / 1.07 / 3.1 | n/r |
| **R, A, V, C 100/50/50 (default)** | 4.9% | 8.6% | 0.61 | -10.9% | 7.6x | 0.43% | 14.7 / 9.2 / -7.4 / 1.60 / 3.0 | 13.4 / 7.7 / -5.9 / 1.73 / 2.9 |
| same, 84-session lookback (previous run) | 5.6% | 8.4% | 0.68 | -11.6% | 7.4x | 0.43% | | |
| R, A, V, C 100/80/60, fitted by the authors on 2005-12 (out-of-sample here) | 3.4% | 6.7% | 0.54 | -11.9% | 6.4x | 0.37% | 13.0 / 7.4 / -5.2 / 1.76 / 2.6 | n/r |
| same 100/80/60, lev 2, 3% interest, tc 0.1% | 2.7% | 13.4% | 0.27 | -27.3% | 13.0x | 4.32% | 22.6 / 14.7 / -10.7 / 1.54 / 2.6 | 21.6 / 14.5 / -12.9 / 1.49 / 2.1 |
| R, A, V, C 100/50/50, log loss (eq. 3) | 8.0% | 10.5% | 0.78 | -12.7% | 6.4x | 0.37% | n/r | n/r |
| SPY buy and hold (no costs) | 14.9% | 17.5% | 0.88 | -33.8% | 0 | 0 | | |

Here each factor the paper adds lowers return: R only is the best FAA row, and the full RAVC default returns less than R, R + A or RAV. Drawdown falls with A
and V as in the paper, but C buys nothing extra. The authors' fitted 100/80/60 weights, tested out of sample, are worse
than the default. Leverage at a fixed 3% roughly doubles volatility and drawdown for less return, because the unlevered
model earns barely more than its financing.

Comparing with the paper: its Sharpe is S0 (0% hurdle, as ours); its D is a monthly-sampled drawdown (ours is daily, so
deeper); its T looks one-sided (ours counts buys and sells, about 2x); its unlevered rows are before costs.

The log form ranks differently from the rank form in practice: over 125 month-ends the top 3 differs in 84 and the final
weights (after the cash rule) in 74. In eq. 3, ln(r/rmax) dominates the V and C terms, so it behaves close to R + A
with a volatility tilt. r <= 0 scores worst there, since ln is undefined (the paper notes this but gives no rule).

## Sensitivity (RAVC 100/50/50), 2016-07-29 to 2026-10-30

Sensitivity only: these runs did not choose any parameter. Common start so that the 6-month lookback has history.
CAGR / Sharpe / Max DD:

| N \ lookback | 3 months | 4 months | 6 months |
|---|---|---|---|
| 2 | 6.6% / 0.70 / -17.9% | 3.2% / 0.37 / -18.9% | 5.0% / 0.55 / -14.9% |
| 3 | 5.8% / 0.70 / -11.9% | 4.8% / 0.60 / -10.9% | 4.9% / 0.61 / -15.7% |
| 4 | 6.7% / 0.90 / -8.5% | 6.4% / 0.86 / -13.5% | 5.5% / 0.67 / -17.8% |

The paper's choice (N=3, 4 months) is not the best cell here; no cell comes near the paper's figures.

## Differences from the paper

- Lookback: the paper measures 4 calendar months, month-end to month-end. The previous run used 84 sessions; this run
  uses month-ends (18 of 125 decisions change, CAGR 5.6% -> 4.9%). The 84-session row is kept for comparison.
- Fills: the paper trades at the next open, the engine at the next close.
- Leverage: modelled as 2x weights with negative cash charged 3% a year (`Costs.margin_bps`) and tc as 10 bps slippage.
  The levered SHY sleeve follows the paper. A fixed 3% is harsher than real rates in 2016-21 and milder than in 2023-24.
- The paper is inconsistent with itself: par. 14 calls 100/80/50 the "best" weights while par. 12-13 use 100/80/60;
  par. 11 quotes RAV as 12.1% / 10.4% against 12.5% / 11.4% in par. 9; the benchmark is 5.6% in par. 5 and 5.7% in
  par. 12; the cash rule is r <= 0 in par. 6 and r < 0 elsewhere (we use r < 0).

Caveats: data starts 2016-01, so the test is 10.4 years, much shorter than the paper's, with no big stock/bond crash
except 2020 and 2022. ETFs are survivors by construction. One path, not evidence of an edge. Sharpe uses a 0% risk-free
rate (as everywhere in this repo).
