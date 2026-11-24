# Munger-style 200-week moving average (S&P 500)

Rules: on each month-end, with the S&P 500 point-in-time panel, a stock is bought when it is high quality AND its price is at or
below its 200-week MA (mean of the last 200 weekly closes, adjusted prices). Held until price is at least X = 20% above the
MA (X fixed in advance, not tuned), then sold. Equal weight among holdings, monthly rebalance, fill next session. Cash
otherwise (0% return, 100% cash when nothing qualifies). Needs 200 weeks of history so signals start 2019-10 (panel starts 2016-01).

High-quality proxy (EDGAR, only filings dated on or before the decision day): latest fiscal-year ROE (net income / equity)
> 15%, debt/equity < 1 (long-term debt plus current portion over equity; a missing debt tag counts as zero debt, biased toward
passing), and positive net income in each of the last 5 fiscal years. Munger himself held businesses for decades, so this
is a loose proxy, not his judgment. About 80-125 of ~500 members pass each quarter.

Data: Alpaca daily bars, SEC EDGAR companyfacts (`edgar.py`, cached in `data/edgar/`). `munger_rules.py`, `run.py`.

Caveats: 601 of 726 panel tickers have EDGAR data, so delisted names are underrepresented (survivorship bias). The
200-week window is only 7 years of results, a single regime, and quality names rarely sit at the 200-week MA, so
holdings swung from 8 to 51 and some months it was nearly all cash. ROE is flattered by buybacks. Not an edge claim.

| 2019-10-25 to 2026-10-30 | CAGR | Vol | Sharpe | Max DD | Turnover/yr | Costs/yr |
|---|---|---|---|---|---|---|
| Munger 200WMA | 12.5% | 24.3% | 0.61 | -38.6% | 2.65x | 0.25% |
| SPY buy and hold | 15.6% | 19.4% | 0.85 | -33.8% | 0 | ~0 |
| Equal-weight S&P (monthly) | 11.8% | 20.5% | 0.65 | -39.9% | 0.87x | |
| Cash (0%) | 0 | 0 | | 0 | | |
