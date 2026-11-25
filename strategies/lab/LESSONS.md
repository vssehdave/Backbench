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

- **05 (inverse-vol QLD/GLD, weekly, 20-day vol target 12%, rest in SHY), WIN.** Holdout CAGR 21.2%, Sharpe 1.48,
  Sortino 2.11, alpha +10.6%, beta 0.57, maxDD -12.3%, MC p95 DD 20.9% (SPY 25.1%); traded every week (446 fills).
  Why it works: (1) gold is the diversifier that paid in both periods; (2) leverage inside a 2x ETF is cheap;
  (3) a 20-day vol scaler reacts in days, and because it keys off volatility rather than price it re-levers as vol
  calms, even without a new high, so it did not miss the rebound the way 04's 200-day filter did. Cost: turnover
  5.5x a year (0.28%/yr in costs), which is affordable. Honest caveat: the 03 -> 04 -> 05 sequence was shaped by
  seeing the 03 and 04 holdouts, so this is a weaker out-of-sample test than a single-shot design. Round 2 should
  confirm it on data neither period has seen (e.g. 2008-2015 with longer history) before trusting it.

- **06 (dual momentum across 8 ETFs incl. 2x, monthly), LOSS.** In-sample Sharpe 0.77 (below SPY); holdout CAGR 20.2%
  but beta 0.99 and Sharpe 1.03. Equal weights with two 2x sleeves in the pool mean the picks are mostly 2x equity
  whenever equities trend, so risk is concentrated, not diversified; monthly absolute momentum also lags the fast
  shocks (2018 Q4, 2020, Apr-2025). Same verdict as the catalog's momentum family: momentum ranking alone adds little
  over SPY after costs; it is the risk weighting (inverse vol, fast vol target) that carried 05. Next: keep 05's risk
  engine and test whether a different diversifier set holds up, or whether it is just "QLD + gold".

- **07 (vol-managed SPY/SSO, no diversifier), LOSS on every check.** In-sample Sharpe 0.77, holdout 0.89, alpha -1.1%.
  Equity vol clusters, but the best rebound days come right after the spikes when exposure is cut, so on a single
  index the vol scaler gives back about what it saves, and at 8x turnover it pays 0.4%/yr in costs. This isolates
  05's edge: the fast vol scaler is a risk limiter, not a return source; the return came from the QLD + GLD
  inverse-vol mix (two low-correlated return streams). Vol timing without a diversifier is not worth it.

- **08 (05 with SSO in place of QLD, untuned), passes all five checks; correlation 0.98 with 05, so not a separate
  winner.** In-sample Sharpe 1.01 (05: 1.10), holdout Sharpe 1.45. This is the most useful result of the round: with
  parameters fixed before the run, the engine works on the S&P too, so 05 is not just a Nasdaq bet. The edge lies in
  the structure (cheap 2x equity + gold, inverse-vol, fast vol cap), not in the choice of index. All the 03/05/08
  variants are one bet (pairwise corr 0.95-0.98); a second winner must come from a different return stream.

## Round 1 summary

1. Cheap leverage plus a real diversifier is what beats SPY here: 2x equity ETFs (financing near T-bill rates) mixed
   inverse-vol with gold. Margin at 5% (02) ate the gain; one index without a diversifier (01, 07) never beat SPY.
2. Brakes must key off volatility and act fast (20-day window, weekly): the 200-day price brake (04) whipsawed in the
   V-shaped Apr-2025 drop, while the vol scaler (05) cut and re-added risk in time.
3. Ranking or timing alone (06 momentum, 07 vol timing) did not beat SPY after costs; the edge came from portfolio
   construction, not from signals.

Round 2: test 05/08 on longer history (2008-2015, which neither period has seen); a second return stream uncorrelated
with 05 (e.g. trend on commodities and FX, carry), so a separate winner is possible; check the gold dependence
(the 2024-2025 gold run flatters the holdout).

## Round 2

- **2008-2015 check of 05/08: not run.** Alpaca, the repo's only daily source (docs/alpaca.md, catalog_data.py),
  returns no bars before 2016-01-04 for QLD, SSO, GLD or SHY, so the 2008 crash cannot be replayed without adding a new
  data source. Until then 05 has only 2016-2026 evidence, part of which shaped its design.

- **09 (05 with TLT in place of GLD), diagnostic, fails all five.** In-sample Sharpe 0.76 (05: 1.10); holdout CAGR
  2.8%, Sharpe 0.28, alpha -6.0% (05: 21.2%, 1.48, +10.6%), same QLD sleeve (~22% average weight). Swapping one asset
  moved holdout CAGR by 18 points, so most of 05's 2024-26 result is gold's run, not the engine. Long Treasuries are no
  longer a diversifier: stock-bond correlation was positive, so inverse-vol put ~2/3 in TLT, which lost money.

- **10 (05 with IEF in place of GLD), diagnostic.** In-sample Sharpe 0.63; holdout CAGR 5.7%, Sharpe 0.76, maxDD -6.2%.
  Safer than TLT but it earns little: the vol cap is barely binding and IEF's low vol pulls most of the weight. Taken
  with 09, the answer to "how much of 05's holdout is gold": with a bond in gold's place the same engine makes 3-6% a
  year instead of 21%, so roughly 15-18 of 05's 21 points of holdout CAGR came from holding gold through its
  2024-2026 run. 05 is a "2x equity + gold" bet with a good risk engine, not an engine that wins with any diversifier.

- **11 (multi-asset trend), LOSS, corr with 05 0.70.** In-sample Sharpe 0.46 (CAGR 1.4%); holdout CAGR 4.0%, Sharpe 1.05, maxDD -3.4%. Unlevered trend on ETF proxies is a smooth but tiny return; the holdout Sharpe came mostly from gold trending, which is why it correlates 0.70 with 05. It would need ~3x leverage to match SPY's CAGR, which the no-margin rule does not allow.

- **12 (credit carry, HYG/EMB with 05's brake), LOSS, corr with 05 0.56.** In-sample Sharpe 0.39 (maxDD -20%, the 2020 credit crash got through the 20-day brake); holdout CAGR 5.6%, Sharpe 1.07, Sortino 1.56, passes four of five but not CAGR. Credit carry is a modest, partly equity-like premium (beta 0.23-0.32); without leverage it cannot reach SPY's CAGR.

- **13 (sector momentum with 05's brake), LOSS, corr with 05 0.55.** In-sample Sharpe 0.65 (CAGR 7.7%); holdout CAGR 11.7%, Sharpe 0.94, Sortino 1.29, beta 0.60. Same answer as the catalog's sector momentum: ranking sectors adds nothing over SPY, and weekly re-ranking turns over ~16x a year. The brake keeps drawdown below SPY's but, unlevered, leaves the return short.

- **14 (factor-ETF momentum, top 1, with 05's brake), LOSS by MC p95 DD only, corr with 05 0.66.** In-sample Sharpe 0.62 (below SPY's 0.78, alpha -0.2%); holdout CAGR 18.2%, Sharpe 1.13, alpha +5.2%. The holdout beat looks like luck of the period, not a stable edge: in-sample it lost to SPY, and top 1 was picked as the best of six tuned levels. Holding one equity factor at a time keeps beta 0.77, so the bootstrap tail is SPY-like (25.9% vs 25.1%). Not a second return stream.

- **15 (05's engine on defensive equity), LOSS, corr with 05 0.30.** The 2x defensive sector ETFs (UGE/RXL/UPW) were worse in-sample than the plain SPLV/USMV pair (Sharpe 0.51-0.57 vs 0.78; 2x decay and 30-38% drawdowns), so the frozen level is unlevered. Holdout: low risk (DD -8.9%, beta 0.34) but CAGR 9.2%. The lowest correlation with 05 so far, but without leverage it cannot clear the CAGR bar, and the levered version was the loser.
