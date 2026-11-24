# 60-day momentum (SPY, QQQ, BTC)

Rules: signal = close / close 60 trading days ago - 1 (`mom60_rules.py`). Positive: fully long. Zero or negative: all cash. Evaluated at
each close, traded at the next session open via the single-instrument harness (`harness.replay`, IBKR-like fees from
`manifest-<name>.json`, `costs: equity_ibkr`). `run.py` re-sizes the position to equity every 21 sessions so the run compounds
(money.Plugin sizes against starting cash only); 98% of equity is deployed to leave room for the open gap and fees.

Data: Alpaca daily SIP bars for SPY and QQQ (2016-01 to 2025-12). BTC is Kraken OHLC, which serves only the latest 720 daily
bars, so BTC covers 2024-12-04 to 2026-11-23 (about 2 years, a falling market), far too short to conclude anything.
BTC trades 7 days a week, so "60 trading days" is 60 daily bars there.

Caveats: buy-and-hold here is price only (no dividends, same as the strategy); cash earns 0%, no interest. A few segment
ends had a share target that could not be filled (SPY 5, QQQ 7, BTC 2 of about 120 segments), a harness limit.
Momentum cut drawdowns but lagged buy and hold in the two stock indices.

| Instrument, period | Strategy CAGR | Vol | Sharpe | Max DD | Turnover/yr | Fees/yr | Buy-hold CAGR | B&H Vol | B&H Sharpe | B&H Max DD |
|---|---|---|---|---|---|---|---|---|---|---|
| SPY 2016-01 to 2025-12 | 9.5% | 10.6% | 0.91 | -19.1% | 7.6x | 0.07% | 12.7% | 17.4% | 0.78 | -33.5% |
| QQQ 2016-01 to 2025-12 | 11.5% | 14.3% | 0.83 | -17.8% | 7.2x | 0.06% | 18.6% | 22.1% | 0.88 | -35.4% |
| BTC 2024-12 to 2026-11 | 0.6% | 19.2% | 0.12 | -29.0% | 11.8x | 3.1% | -20.9% | 35.8% | -0.27 | -52.8% |
| Cash | 0 | 0 | | 0 | | | | | | |

BTC fees are a high share because the account is 10,000 USD and the minimum commission applies.
