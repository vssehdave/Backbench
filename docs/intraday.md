# Intraday backtests

`intraday.py` holds the shared code: calendar and daily bars from Alpaca SIP, the monthly universe, overnight and
intraday legs, the ORB day logic, sizing, fees, metrics. Strategies live in `strategies/intraday/overnight` and
`strategies/intraday/orb`; each has a README, manifest, `results.json` and `run.py`. Tests: `test_intraday.py`.

- Daily open and close come from SIP 1Day bars (official auction prints). Minute bars are used only for ORB and the
  extended-hours variant, cached under `data/intraday/` (ignored by git).
- Calendars come from the trading calendar, including half days.
- Decisions use closed bars only; ORB fills at the next minute's open.
- SIP is refused for ranges ending today, so runs end at the last full session (2026-11-20).
- A rerun reuses the cache; the first run is slow (ORB about 21 minutes, overnight about 32).
