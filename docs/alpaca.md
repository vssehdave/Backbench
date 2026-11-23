# Alpaca historical bars

`python harness.py --alpaca --symbol QQQ --start 2022-01-01 --end 2024-01-01` fetches one-minute bars from Alpaca Market Data v2 (`feed=sip`, `adjustment=raw`) and checks them for coverage, and takes each session's open and close from Alpaca `1Day` raw SIP bars. Prices are as-traded USD. Minute bars are not used for prices: the 16:00 closing-auction print is stamped into the 16:00 ET minute bar, so the last in-session minute close misses the official close. Reports use `source = "alpaca_sip_raw"`; `data_quality` mirrors `--minute-csv` and adds feed, adjustment, fetch time, payload sha256 and corporate actions.

Keys come from `APCA_API_KEY_ID` and `APCA_API_SECRET_KEY`, falling back to the git-ignored `.env`. They are sent as headers only and never cached or reported. HTTP 429 is retried with bounded backoff. A 401 or 403 stops the run; the free plan may restrict recent SIP data.

Raw response pages are cached in `data/alpaca/` (override with `--alpaca-dir`), one file per symbol, range and feed, with request parameters and a sha256 that is rechecked on every read. Delete the file to refetch. Do not cache a range that ends in the future. Cached files are about 50 MB for two years of QQQ and stay outside Git.

Splits and dividends come from `/v1/corporate-actions` and are listed in `data_quality`. A split inside the range stops the run, since as-traded prices jump across it; `--allow-splits` accepts it and records it. Dividends are recorded, not applied, so the replay carries no dividend cash flows. Missing minutes and exchange holidays still need separate verification.

Session hours come from Alpaca's trading calendar (`GET {APCA_API_BASE_URL}/calendar`, cached in the same file and covered by the sha256). Minute bars from each session's calendar open up to its close count towards coverage. The `1Day` dates must equal the calendar sessions or the run stops. A calendar session with no bars, or a regular-hours bar on a date outside the calendar, stops the run. `early_closes` lists shortened sessions. `sessions_short_of_calendar` replaces `sessions_under_390` and compares observations with the minutes the calendar expects.

Cross-check, QQQ 2022-01-01..2024-01-01, Alpaca versus the independent minute CSV (`python crosscheck.py CSV QQQ START END`):

| | Sessions | Median bps | Max bps | Over 5 bps |
|---|---|---|---|---|
| Open | 501 (none unmatched) | 0 | 0.18 | 0 |
| Close | 501 (none unmatched) | 0 | 3.45 | 0 |
