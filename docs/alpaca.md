# Alpaca historical bars

`python harness.py --alpaca --symbol QQQ --start 2022-01-01 --end 2024-01-01` fetches one-minute bars from Alpaca Market Data v2 (`feed=sip`, `adjustment=raw`) and aggregates them to regular-hours daily bars: first open from 09:30 Eastern, last close before 16:00. Prices are as-traded USD. Reports use `source = "alpaca_sip_raw"`; `data_quality` mirrors `--minute-csv` and adds feed, adjustment, fetch time, payload sha256 and corporate actions.

Keys come from `APCA_API_KEY_ID` and `APCA_API_SECRET_KEY`, falling back to the git-ignored `.env`. They are sent as headers only and never cached or reported. HTTP 429 is retried with bounded backoff. A 401 or 403 stops the run; the free plan may restrict recent SIP data.

Raw response pages are cached in `data/alpaca/` (override with `--alpaca-dir`), one file per symbol, range and feed, with request parameters and a sha256 that is rechecked on every read. Delete the file to refetch. Do not cache a range that ends in the future. Cached files are about 50 MB for two years of QQQ and stay outside Git.

Splits and dividends come from `/v1/corporate-actions` and are listed in `data_quality`. A split inside the range stops the run, since as-traded prices jump across it; `--allow-splits` accepts it and records it. Dividends are recorded, not applied, so the replay carries no dividend cash flows. Missing minutes and exchange holidays still need separate verification.

Session hours come from Alpaca's trading calendar (`GET {APCA_API_BASE_URL}/calendar`, cached in the same file and covered by the sha256). Only bars from each session's calendar open up to its close count, so after-hours prints on early-close days never become the close. A calendar session with no bars, or a regular-hours bar on a date outside the calendar, stops the run. `early_closes` lists shortened sessions. `sessions_short_of_calendar` replaces `sessions_under_390` and compares observations with the minutes the calendar expects.
