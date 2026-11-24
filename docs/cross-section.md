# Cross-sectional testing

`xs_data.py` builds the panel, `xsection.py` is the engine, `strategies/xs/` holds the two reference strategies.
Run one with `python money.py xs strategies/xs/momentum_12_1.json` (or `python xsection.py ...`). Reports go to
`reports/xs_<id>.json`, which is git-ignored, so this page is the committed record of the run below.

## RESULTS ARE SURVIVORSHIP-BIASED

The universe is reconstructed from Wikipedia, not from a licensed point-in-time index file. Coverage is high but not
complete and ticker identity is not verified (see Limits). Treat every number here as an engineering check, not evidence
of an edge. Momentum and low-volatility are paper defaults and were not tuned.

## Data

- Bars: Alpaca daily SIP via `/v2/stocks/bars` for many symbols, 100 per request, paged and merged per symbol, cached
  under `data/alpaca_xs/` with a sha256 of the bars checked on every read. Two pulls: `adjustment=all` (split and
  dividend adjusted) and `adjustment=raw`. The cache holds only `[date, close]`, not the raw JSON pages.
- Adjusted close drives signals, returns, marking and the benchmarks. Raw close is used only to turn traded value into a
  share count for per-share commissions and regulatory fees. Both pulls must cover identical dates per symbol.
- The request started 2015-01-01 to give momentum a warm-up, but Alpaca returned nothing before 2016-01-04. The
  first fold's test window therefore has no 12-1 history, and both strategies abstain (cash, 0%, Sharpe n/a) in
  2016H2. That row is "insufficient history", not a result.
- Membership: current list (Wikipedia "List of S&P 500 companies", revision 1384572480) with every later change undone
  using the "Historical components of the S&P 500" changes table (revision 1387311792). Pages are cached under
  `data/sp500/` with sha256. The current list is as of fetch, so all changes dated after it were undone too.
  Membership size on sampled dates was 509 (2016), 507 (2020), 503 (2026). 5 changes contradicted the running set.
- Panel: 726 tickers, 2,723 sessions (2016-01-04 to 2026-10-30), 78 MB of cache, about 11 minutes for the full pull.
- Tradable at decision date t means: member after t's close and has a bar on t. A held name with no bar is carried at
  its last price through gaps; once past its final bar in the dataset it is closed at that last price with costs.

## Survivorship coverage (2016-01-04 to 2026-10-30)

- 725 tickers were members at some point; 0 have no Alpaca bars at all; 17 have bars that start after membership
  began: AA, ANDV, APTV, BBWI, CTRA, DAY, FTI, LIN, Q, SKYD, SNDK, STI, TE, TFCF, TFCFA, UAA, VTRS. These are mostly
  renamed or re-formed companies whose earlier history sits under another ticker. 0 end before removal.
- 99.07% of member-days have a price (1,365,024 of 1,377,890). The missing 0.9% is those 17 names before their
  data starts. Flag: biased.
- Not measured: a ticker reused by a different company would show full coverage while being wrong. 107 adjusted
  daily moves above 50% were counted in the panel (spin-offs, failed names, possible splices) and are not resolved.

## Engine

- Strategy: `decide(as_of, params) -> {symbol: weight}` (negative is short; `None` abstains). Optional `fit(as_of, level)`
  returns the artifact passed as `params`. `as_of` holds only the members with a bar that day, with adjusted
  closes up to and including that date. Nothing later exists in the object (tested, with a positive control).
- Timing: decide at the close of the last session of the month (or ISO week), trade at the next session's close.
- Limits per manifest: per-name cap, net, then gross, applied by the engine. Weights for symbols outside the as-of
  universe raise an error.
- Costs: commission 0.0035 USD per share, 0.35 minimum, capped at 1% of trade value; sell-side regulatory estimate
  (0.00206% of sale value plus 0.000003 per share); 5 bps slippage per trade; short borrow 50 bps a year on short market
  value (general collateral), accrued per calendar day; optional `margin_bps` (default 0) on negative cash, booked as
  borrow. The fee profile name is `ibkr-tiered-like-2026-11-23`; the
  numbers mirror `harness.py` and are an estimate, not a statement.
- Dividends: handled through the adjusted-price return, which is equivalent to immediate reinvestment. Dividends owed
  on short positions, withholding and cash timing are not modelled.
- Accounting: one cash balance, daily mark-to-market on adjusted prices. Each fold starts from 1,000,000 USD of cash.
- Folds: same schedule as `harness.py` (6 month selection, 6 month test, 12 month steps from 2016-01-01). Both
  strategies have one parameter level, so selection runs but cannot change the choice.
- Benchmarks: equal-weight buy-and-hold of the universe at the start of the test window (no costs, no rebalancing),
  SPY buy-and-hold, and cash.

## Strategies (paper defaults)

- `xs_momentum_12_1`: score = close 21 sessions ago over close 252 sessions ago; long top decile, short bottom decile,
  equal weight, 0.5 each side, gross 1, net 0, name cap 5%, monthly.
- `xs_low_volatility`: long-only, equal weight in the 20% with the lowest 252-session daily-return standard deviation,
  gross 1, net 1, name cap 5%, monthly.

## Results, test windows

Return is net of costs. Mom = momentum long/short, LV = low volatility, EW = equal-weight universe, SPY.
Dashes are the 2016H2 insufficient-history fold. Cash is 0% in every window.

| Test window | Mom | Mom Sharpe | LV | LV Sharpe | EW | SPY |
|---|---|---|---|---|---|---|
| 2016-07..2016-12 | - | - | - | - | 8.8% | 7.9% |
| 2017-07..2017-12 | 0.1% | 0.07 | 8.5% | 2.98 | 9.9% | 11.5% |
| 2018-07..2018-12 | 1.7% | 0.45 | 0.4% | 0.12 | -9.1% | -6.9% |
| 2019-07..2019-12 | -4.1% | -0.62 | 6.9% | 1.40 | 8.2% | 10.9% |
| 2020-07..2020-12 | -13.1% | -0.84 | 13.2% | 1.99 | 26.7% | 22.1% |
| 2021-07..2021-12 | -2.7% | -0.46 | 12.7% | 2.32 | 8.6% | 11.7% |
| 2022-07..2022-12 | 3.5% | 0.53 | 2.7% | 0.39 | 6.3% | 2.3% |
| 2023-07..2023-12 | -3.7% | -0.73 | 1.5% | 0.35 | 6.4% | 8.0% |
| 2024-07..2024-12 | 1.8% | 0.45 | 9.1% | 1.89 | 7.6% | 8.4% |
| 2025-07..2025-12 | 5.3% | 0.97 | -1.9% | -0.36 | 7.2% | 11.0% |

Per fold cost drag was about 0.37% of start cash for momentum (turnover about 8x a year on about 98 names) and about
0.12% for low volatility (turnover about 3.7x). Momentum leg returns (long / short, percent of start cash): 2020H2
+8.3 / -21.1 (the November 2020 momentum reversal), 2018H2 -7.5 / +9.5. Volatility, maximum drawdown, leg returns,
forced closes and the decision log per fold are in the JSON reports. Sharpe on six months of daily returns is noisy;
do not rank strategies by it.

## Limits and what was left out

- Ticker identity over time is trusted: no check that an old ticker is the same company. Wikipedia is not a licensed
  point-in-time source. Names that failed (for example SIVB) are closed at the last traded price, which overstates
  recovery.
- No fractional-share rounding, no borrow availability or hard-to-borrow rates, no market impact beyond a flat
  slippage, no intraday timing, no dividend cash on shorts.
- Each fold restarts at cash, so folds are not chained into one equity curve.
- `money.py` only gained an `xs` subcommand that hands over to `xsection.py`; xs manifests have their own schema,
  validated in `xsection.py`, not the `money.py` manifest fields.

## Tests

`python -m unittest test_xsection` (offline, synthetic panels): no lookahead with a positive control, as-of view,
commission minimum and cap, per-share and slippage arithmetic by hand, borrow fee across a weekend, weight limits,
delisting close, a one-day gap, membership gating, schedule and folds, deterministic rerun, fit sees only prior data,
manifest validation, both strategies, membership reconstruction, table parsing and coverage.
