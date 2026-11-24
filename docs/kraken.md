# Kraken daily bars (24/7 crypto)

`kraken_bars.daily_from_kraken(pair)` reads Kraken's public `GET /0/public/OHLC?pair=XBTUSD&interval=1440` (no key) and returns `(date, open, close)` rows per UTC day plus a quality dict. Manifests use `data.kind = "kraken"`, `data.symbol` = the pair, and must set `calendar = "utc24"` (anything else is rejected). See `strategies/btc_threshold.json`.

**History limit.** Kraken returns only the 720 most recent candles whatever `since` is, so it cannot reach 2022. Checked 2026-11-24: XBTUSD runs 2024-12-04 to 2026-11-23 (720 sessions, 206 weekend days, no gaps). The earliest date moves forward one day per day, so pass a `--start` after it. Older history needs another source (Kraken's downloadable trade/OHLCVT files); nothing is backfilled or faked.

Open is the candle's first trade, close its last, in USD. The still-open current-day candle is dropped. Missing UTC dates between first and last raise unless `allow_gaps=True`. `data_quality` lists session count, first and last date, missing dates and weekend sessions.

The raw response is cached in `data/kraken/<PAIR>_<fetch date>_raw.json` with url, params, fetch time and a sha256 that is rechecked on every read; a mismatch stops the run. One fetch per pair per UTC day. Kraken answers errors with HTTP 200 and an `error` list; rate limits are retried, other errors raise. The result key can differ from the requested pair (`XXBTZUSD` for `XBTUSD`), so the single series is taken whatever its name.

Costs in the manifest (26 bps, 0.0001 lot) are assumptions to verify against the account's Kraken fee tier.
