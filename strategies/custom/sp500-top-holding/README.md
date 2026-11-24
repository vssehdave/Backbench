# S&P 500 largest-company holding

Rules: each session compute market cap for every S&P 500 member (point-in-time panel); hold 100% of the largest. When the
leader changes, sell everything and buy the new one. Decision uses data through day t-1 (1-day lag), fill at the next
session. Daily check. Costs: IBKR-like fees plus 5 bps slippage.

Data: Alpaca daily SIP bars (S&P 500 point-in-time panel 2016-2026) and SEC EDGAR XBRL companyfacts (keyless, cached in
`data/edgar/`, generic User-Agent, under 10 requests/s; modules `edgar.py`, `fetch_edgar.py`, `leader_rules.py`).
Shares: `dei:EntityCommonStockSharesOutstanding`, falling back to `us-gaap` shares. A figure is usable only from its
filing date, never its period end. Share classes on one cover page are summed (Alphabet, News Corp). Market cap = shares x raw
close at the period end x adjusted-price ratio since then (carries splits forward without lookahead). Values more than 100x
from a company's own median are dropped (some filings report counts 1000x too large, e.g. GRMN, TFC).

Caveats: survivorship bias remains for names missing from EDGAR (125 of 726 panel tickers have no CIK or no facts, mostly
delisted or acquired, so 601 are covered); the leader is always a large, living company so this matters little for the top spot
but not zero. Shares are quarterly and cover dates up to ~50 days stale. Flip-flops in 2019-2020 and 2024-2025 are real
near-ties among Apple, Microsoft, Amazon and Nvidia, and each switch costs slippage plus a day of lag. Holding one stock
gives 30% volatility.

Timeline sanity check (see `results.json`): Apple leads from 2016, Microsoft and Amazon trade places with Apple from
Dec 2018 (true: Amazon and Microsoft both passed Apple briefly in late 2018 and Jan 2019), Microsoft leads through 2021,
Apple again 2022-2023, Microsoft Jan 2024, Nvidia first takes the top spot 2024-06 and holds it from 2025. Days as leader:
AAPL 2740, MSFT 589, NVDA 512, GOOG 91, AMZN 19. One doubtful item: Alphabet (GOOG) shows as leader for 91 days in 2022
which is wrong in reality (it was #3), likely from summing share classes while price is for one class.

| 2016-01-04 to 2026-10-30 | CAGR | Vol | Sharpe | Max DD | Turnover/yr | Costs/yr |
|---|---|---|---|---|---|---|
| #1 holding | 13.4% | 30.3% | 0.57 | -52.4% | 10.3x | 0.54% |
| SPY buy and hold | 14.7% | 17.4% | 0.88 | -33.8% | 0 | ~0 |
| Cash (0%) | 0 | 0 | | 0 | | |

56 leader switches. The strategy underperformed SPY with 1.7x the volatility.
