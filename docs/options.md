# Options backtest (chapter 2 fixed-structure strategies, 2.2 to 2.57)

`options_bt.py` rolls one option position per month on SPY against 200 shares bought at the first expiry's close (USD 100,000 start, same shares and dates for the buy-and-hold comparison). `options_data.py` fetches and caches the inputs under `data/alpaca_options/` as raw pages with a sha256 re-verified on load. Offline tests: `python -m unittest test_options_bt`. Real run (needs Alpaca keys): `python options_bt.py`; it writes `options_results.json` into the 2.2 and 2.4 catalog folders.

## Rules

- Roll date is the monthly expiry (third Friday, or the previous session when that Friday is a holiday). The new contract is the next monthly expiry (28 to 35 days).
- Strike: nearest listed strike to spot x 1.02 (short call) or spot x 0.95 (long put), spot being that day's SPY close.
- Entry at the contract's daily bar close plus or minus a half-spread (USD 0.02 per share, **an assumption**: there are no historical quotes, so the real spread is unknown; results at 0, 0.05 and 0.10 are recorded). Fee USD 0.65 per contract on opening trades only.
- Hold to expiry, settle at intrinsic value against the SPY close. An ITM short call counts as assignment, with the shares rebought at the same close, which nets to the intrinsic loss. No fee on settlement.
- If the chosen contract has no bar on the roll day, entry slips to its first later bar and the missing sessions are counted (`no_bar_days`); with no bar all cycle, the shares stay unhedged. Days without a bar while the option is held are counted as `mark_gap_days` and marked at the last close.

## Data facts (checked with the free keys)

- Option bars exist only from 2024-01-18. `/v1beta1/options/bars` works; there is no historical bid/ask or implied volatility. The `opra` snapshot feed returns 403.
- Contract listing works through the trading API, `GET https://paper-api.alpaca.markets/v2/options/contracts`, but expired contracts appear only with `status=inactive`. `status=expired` returns an empty list with no error.
- Daily SPY closes come from the stock bars endpoint (SIP, raw). SIP returns 403 for a range ending today, so the run ends at the last settled expiry.

## Limitations

- About 2.8 years and 34 cycles, one bull-market regime: low confidence. Differences from buy-and-hold are not statistically meaningful.
- Bars are trade closes, not quotes; an illiquid strike's last trade can be stale or off-market, and the half-spread is a guess.
- Price return only: SPY dividends (about 1.3% a year) and interest on cash are ignored, for the options and the benchmark alike. Share purchases carry no commission.
- European-style settlement only: no early exercise or ex-dividend assignment (SPY options are American).
- Whole-lot sizing (200 shares) leaves little cash and a fixed hedge ratio; margin and collateral are not modelled.
- One strike rule per strategy; no parameter search, so nothing here is tuned, but nothing is robust across rules either.

## Multi-leg catalog (all 58 chapter-2 folders)

`STRATEGIES` in `options_bt.py` defines each strategy as legs of (kind, quantity, strike offset from spot, far expiry). Kinds are call, put and stock; negative quantity is short. Strike step S is 2.5% of spot (half step 1.25%) because the paper gives no strikes; nothing is tuned, and 2.2 and 2.4 keep their original 2% and 5% OTM strikes. Strikes snap to the listed strike nearest the target. Calendars and diagonals buy the following expiry as the far leg and close it at the near expiry at its trade close, so they lose the last cycle. One missing leg skips the whole cycle (reported as opened n/N). Each long or short ITM leg is cash-settled at expiry; short ITM legs count as assignments. Fees are 0.65 USD per contract per leg, and half-spread 0.02 USD per share is paid on every leg open and close. Mark-to-market uses the last trade close, so illiquid wings show mark gaps; treat results as low confidence. Real run writes `options_results.json` into every chapter-2 folder. Nothing in chapter 2 was left untestable.
