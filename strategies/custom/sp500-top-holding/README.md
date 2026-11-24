# S&P 500 largest-company holding

Rules: each session compute market cap for every S&P 500 member (point-in-time panel); hold 100% of the largest. When the
leader changes, sell everything and buy the new one. Decision uses data through day t-1 (1-day lag), fill at the next
session. Daily check. Costs: IBKR-like fees plus 5 bps slippage.

Data: Alpaca daily SIP bars (S&P 500 point-in-time panel 2016-2026) and SEC EDGAR XBRL companyfacts (keyless, cached in
`data/edgar/`, generic User-Agent, under 10 requests/s; modules `edgar.py`, `fetch_edgar.py`, `leader_rules.py`).
Shares: `dei:EntityCommonStockSharesOutstanding`, falling back to `us-gaap` shares. A figure is usable only from its
filing date, never its period end. Share classes on one cover page are summed (Alphabet, News Corp). Market cap = shares x raw
close on the filing day x adjusted-price ratio since then (carries splits forward without lookahead). Values more than 100x
from a company's own median are dropped (some filings report counts 1000x too large, e.g. GRMN, TFC).

Caveats: survivorship bias remains for names missing from EDGAR (125 of 726 panel tickers have no CIK or no facts, mostly
delisted or acquired, so 601 are covered); the leader is always a large, living company so this matters little for the top spot
but not zero. Shares are quarterly and cover dates up to ~50 days stale. Flip-flops in 2019-2020 and 2024-2025 are real
near-ties among Apple, Microsoft, Amazon and Nvidia, and each switch costs slippage plus a day of lag. Holding one stock
gives 30% volatility.

Multi-class companies: EDGAR companyfacts does not label per-class share values, so shares are the all-class total for one
CIK (one entry per company, so Alphabet is not counted twice) priced with one listed class, the first symbol alphabetically
(GOOG for Alphabet; GOOGL differs by about 1%). Unlisted Class B is covered by the total. Berkshire (no share facts after 2011) and
Meta (no share facts at all) cannot be sized from this data and are excluded; neither was #1 in the period, but the leader is
only the largest among covered companies. Facts older than 400 days are treated as missing.

Fix history: an earlier run showed Alphabet as #1 for 91 days in 2022. The cause was not class summing but a July 2022 filing restating
2021 share counts after the 20:1 split, priced at the pre-split 2021 close (20x too large). Caps are now priced on the filing day.

Timeline sanity check (see `results.json`): Apple leads from 2016; Microsoft and Amazon trade places with Apple from Dec 2018 to
2020 (true: Amazon and Microsoft passed Apple briefly in late 2018 and early 2019, Microsoft in Feb-Mar 2020); Microsoft
Nov 2021 briefly, Apple through 2022-2023 (true), Microsoft Jan 2024 (true), Nvidia from 2024-06 on and again from 2025
(true: first passed Microsoft and Apple in June 2024). Days as leader: AAPL 2831, MSFT 589, NVDA 512, AMZN 19. Alphabet never leads.

| 2016-01-04 to 2026-10-30 | CAGR | Vol | Sharpe | Max DD | Turnover/yr | Costs/yr |
|---|---|---|---|---|---|---|
| #1 holding | 15.0% | 30.3% | 0.61 | -50.7% | 9.9x | 0.52% |
| SPY buy and hold | 14.7% | 17.4% | 0.88 | -33.8% | 0 | ~0 |
| Cash (0%) | 0 | 0 | | 0 | | |

54 leader switches. The strategy edged SPY on CAGR (15.0% vs 14.7%) with 1.7x the volatility and a deeper drawdown.
