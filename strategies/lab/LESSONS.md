# Lab lessons

Evidence: strategies/catalog/INDEX.md (92 tested sections, mostly compounded over ten July-December windows
2016-2026), strategies/custom/INDEX.md (continuous 2016-2026 runs with the standard report), and the lab runs logged in
LOG.md. SPY buy and hold on the lab panel: 2016-2023 CAGR 13.2%, Sharpe 0.78, maxDD -33.8%; holdout 2024-01 to
2026-11 CAGR 16.6%, Sharpe 1.04, Sortino 1.53, maxDD -18.8%.

## What the earlier runs say

1. **Timing SPY alone cuts drawdown but loses return.** Every single-instrument rule on SPY (single, two and three
   moving averages, channel, support and resistance, 60-day momentum) ended below buy and hold: momentum-60d SPY 9.7%
   CAGR vs 12.7%, two MAs 23.4% vs 46.8% over the windows. Beta 0.37 and Sharpe 0.93 show it does what a trend filter
   should (cash in 2018 Q4 and 2022), but it is out of the market about a third of the time in a decade where the market
   rose 13% a year, and it re-enters late after V-shaped recoveries (2020). A trend filter is a risk tool, not a return
   tool: it can only beat SPY on CAGR if the risk it saves is spent on leverage.
2. **Diversifiers earned nothing in 2016-2023.** FAA (Sharpe 0.61, beta 0.26, CAGR 5.0%) and multi-asset trend (-4.8%)
   held bonds, commodities and REITs. TLT returned -0.3% a year and IEF 0.6% in-sample, so any allocation away from US
   equity paid a large return cost. Low beta plus a small positive alpha (+1.2%) is not enough to match a 13% market.
3. **Mean reversion and pairs on ETFs lose.** Contrarian (10.3, -21.3%), ETF mean reversion (4.4, -38.5%), pairs (3.8,
   -7.9%), support and resistance (-23.3%): high turnover at a few bps a side, and in a strongly trending decade the
   losers kept losing.
4. **Cost and turnover kill fast strategies.** Intraday ORB (-22.8% CAGR long-short at 2 bps, -43% for 5-minute top-50)
   and SPY overnight (-2.4%) are cost-dominated. Anything turning over more than ~20x a year needs a per-trade edge
   above 10 bps round trip, which none of these had.
5. **Stock-level cross-sectional factors underperformed equal weight** (price momentum, low vol, residual momentum,
   multifactor: all negative mean 6-month vs +8% equal weight), even with survivorship bias in their favour. Sector
   momentum (4.1 xs) matched SPY on return (CAGR 17.0% vs 17.7% on the same windows) with similar drawdown: no edge.
6. **Leverage was the only thing that beat SPY on return** (4.5 LETFs 29.8% vs 11.4%; QLD 30.1% CAGR in-sample) but
   with drawdowns near -60%, so Sharpe stayed below SPY's.

## Design rules for the lab, from the above

- Beating SPY on Sharpe needs either timing (trend, volatility) or a diversifier that actually earns; beating it on
  CAGR at the same time needs leverage on that better-Sharpe stream. So: improve Sharpe first, then lever it.
- Keep turnover low (monthly or weekly decisions) so 5 bps a side stays a small drag.
- Leverage is charged 5% a year on borrowed cash (COSTS in labkit.py), so it only pays when expected excess return
  is well above 5%.
- Re-enter fast after crashes, or the 2020-style V costs more than the crash saved.

## Lessons from lab runs

(Added after each strategy; newest last.)

- **01 (vol target + trend on SPY), LOSS.** Sharpe 0.76 in-sample vs 0.78 for SPY: on one asset, vol targeting and a
  200-day filter cut maxDD from -34% to -22% but do not raise Sharpe, because SPY's high-vol days are also its biggest
  up days (rebounds), so scaling down after vol spikes misses them. Leverage at 5% a year cost 1.5% of equity a year.
  On the holdout it again cut drawdown (-12% vs -19%) but trailed on CAGR (14.3% vs 16.7%). Next: the Sharpe gain has to
  come from a second return stream, not from timing one asset.

- **02 (levered risk parity SPY/QQQ/GLD/TLT), LOSS by CAGR only.** First design to beat SPY on Sharpe, Sortino, alpha
  and MC p95 DD in the holdout (gold's 2024-2025 run and low correlation did the work). It fell short on CAGR (15.1% vs
  16.7%) because the 12% vol target held gross near 1.4x and the borrowed part paid 5% a year: in-sample the margin
  interest was ~3% of equity a year, more than the whole Sharpe gain. IEF or TLT as the diversifier was worse in-sample
  (TLT -0.3%/yr): bonds were a cost, gold was the useful diversifier. Next: get the leverage cheaper (SSO/QLD carry
  their own financing at roughly T-bill rates, not 5%), or raise return without leverage (higher-return equity sleeve).

- **03 (inverse-vol QLD/GLD, no margin), LOSS by MC p95 DD only (26.2% vs 25.1%).** Moving the leverage from 5%
  margin into 2x ETFs cut financing cost from ~3%/yr to ~0.06%/yr of equity and lifted in-sample Sharpe from 0.79 to
  0.93. Holdout CAGR 22.5%, Sharpe 1.29, alpha +9.2%. Cheap leverage was the missing piece. The remaining failure is
  tail risk: the bootstrap can string together bad equity blocks and a monthly inverse-vol rule has no brake inside
  the month, so the 2x sleeve drives a deeper p95 drawdown than SPY. Next: add a trend brake on the 2x sleeve.

- **04 (03 + SSO + 200-day trend brake, weekly), LOSS.** Best in-sample so far (Sharpe 1.09, CAGR 16.7%, maxDD -20%),
  because 2018 Q4 and 2022 were slow bear markets a 200-day filter catches. The holdout drawdowns were fast
  (Apr-2025, a few weeks): the brake sold near the low and re-entered higher, so holdout Sharpe fell from 1.29 (03) to
  1.07, Sortino to 1.48 and MC p95 DD rose to 29.7%. Adding SSO also raised beta to 0.90. Lesson: a slow trend brake
  helps against slow bears only and costs in V-shaped shocks; the in-sample period had more slow bears than the
  holdout. A brake must react to volatility (fast) rather than price trend (slow), or not exist.
