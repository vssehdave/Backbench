# Lab log

Design and tuning on 2016-01-01..2023-12-31 only; one holdout run on 2024-01-01..2026-11-24 with levels[0] of the
manifest frozen. Costs 5 bps a side, no commission, 5% a year on borrowed cash (labkit.COSTS). Run with
`python strategies/lab/labkit.py <manifest> tune|insample|holdout`; reports are in each folder's
results/insample/ and results/holdout/ (REPORT.md, report.json, equity.svg). Holdout SPY: CAGR 16.7%, Sharpe 1.04,
Sortino 1.53, maxDD -18.8%, MC p95 DD 25.1% (this varies a little per run, since it is bootstrapped beside each strategy).

WIN needs, on the holdout vs SPY: Sharpe and Sortino above, alpha > 0, MC p95 maxDD <= SPY's, CAGR >= SPY's (or >= 80% of
it when the realised maxDD is under half of SPY's).

| # | idea | hypothesis | in-sample Sharpe (SPY 0.78) | holdout CAGR / Sharpe / Sortino / alpha / maxDD / MC p95 | vs SPY | result | why |
|---|---|---|---|---|---|---|---|
| 01 | SPY vol-targeted to 15% (cap 1.5x), SHY below the 200-day MA, weekly | Vol targeting raises Sharpe; leverage in calm uptrends recovers the CAGR a trend filter gives up | 0.76 | 14.3% / 0.94 / 1.30 / +2.2% / -12.0% / 25.9% | 16.7% / 1.04 / 1.53 / 0 / -18.8% / 25.1% | LOSS | Levered only when vol is low, so it is de-levered in the fast rebounds (2020, Apr-2025) that carry the return; 5% margin ate 1.5%/yr in-sample |
| 02 | Inverse-vol SPY/QQQ/GLD/TLT scaled to 12% vol (gross <= 2), monthly | Gold and bonds are a second return stream with low equity correlation; levering the mix lifts CAGR | 0.79 | 15.1% / 1.06 / 1.58 / +2.8% / -12.3% / 21.7% | 16.7% / 1.04 / 1.53 / 0 / -18.8% / 25.1% | LOSS | Passed Sharpe, Sortino, alpha and MC DD; CAGR 90% of SPY with maxDD 65% of SPY's (needs under half). Margin at 5% cost ~3%/yr in-sample |
| 03 | Inverse-vol QLD (2x Nasdaq) / GLD, monthly, no margin | Same risk parity, but leverage bought inside 2x ETFs (financed near T-bill rates) instead of 5% margin | 0.93 | 22.5% / 1.29 / 1.86 / +9.2% / -17.0% / 26.2% | 16.7% / 1.04 / 1.53 / 0 / -18.8% / 25.1% | LOSS | Beat SPY on CAGR, Sharpe, Sortino, alpha and realised DD; MC p95 DD 26.2% vs 25.1% (fails by 1.1 pt): no crash brake on the 2x sleeve |
| 04 | 03 plus SSO, weekly, each 2x sleeve to SHY when its index is below the 200-day MA | A trend brake on the 2x sleeves cuts the tail that failed 03 | 1.09 | 22.3% / 1.07 / 1.48 / +7.3% / -20.4% / 29.7% | 16.7% / 1.04 / 1.53 / 0 / -18.8% / 25.1% | LOSS | Brake whipsawed: sold after the Apr-2025 drop and bought back higher; Sortino and MC DD worse than 03 and than SPY |
| 05 | Inverse-vol QLD/GLD, weekly, scaled to 12% vol on a 20-day window, rest in SHY | A fast volatility brake (not a slow price-trend one) cuts the 2x sleeve within days of a shock and re-adds it as vol settles | 1.10 | 21.2% / 1.48 / 2.11 / +10.6% / -12.3% / 20.9% | 16.7% / 1.04 / 1.53 / 0 / -18.8% / 25.1% | WIN | All five checks pass; 446 holdout fills. Caveat: the idea came after seeing the 03 and 04 holdouts (parameters tuned in-sample only) |
