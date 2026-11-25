# Strategy manifests and the money CLI

Each strategy is a JSON manifest, for example `strategies/threshold.json`. Every field is required and unknown fields are rejected.

| Field | Meaning |
| --- | --- |
| `id`, `version` | Report label and manifest version. |
| `entry` | `module:name`, a `decide(history, level)` function or a class with `fit(rows, level)` and `decide`. The module is imported with the manifest's folder on `sys.path`, so a new package needs only its manifest beside it. |
| `data` | `{"kind": "fixture" \| "spot_fixture" \| "alpaca", "symbol": ...}`. |
| `calendar` | `xnys` or `utc24`; must match the data kind and the cost profile. |
| `warmup` | Bars required before the first decision; earlier bars abstain. |
| `levels` | Parameter grid for the six-month optimize and forward folds. |
| `costs` | `"equity_ibkr"` or `{"fee_bps", "lot", "min_usd"}` (utc24 only). |
| `benchmark` | Recorded in the report; not yet computed. |
| `max_exposure` | In (0, 1]. Caps target position value at this share of the 10,000 starting cash. |

`decide` may return `None` to hold the current position. Abstentions are counted per fold and in total in the report.

```
python money.py test strategies/threshold.json            # validate, run folds, write reports/threshold.json
python money.py replay strategies/threshold.json --start 2023-01-01 --end 2023-04-01 [--level 100]
python money.py compare reports/threshold.json reports/cash.json
```

Validation lists every manifest problem in one error before any data is loaded. Not built yet: experiment registry, portfolio state passed to `decide`, multi-asset.

## Shorting

Single-instrument runs are long-only unless the manifest opts in with `"allow_short": true` (requires `costs: "equity_ibkr"`). Without it a negative target is still an error. Optional `"borrow_bps_per_year"` (default 50, the same general-collateral rate as `xsection.py`) is only valid with `allow_short`.

- Accounting: a short sale credits the proceeds to cash; equity is `cash + shares * price` with shares negative. A long-to-short flip is one order for the full difference. The sell-side regulatory fee applies to short sales as to any sell.
- Borrow: each row after a short is held charges `short value at the previous close * borrow_bps / 10000 * calendar days / 365`, so weekends cost three days.
- Margin guard: `max_exposure` caps the absolute target value (long or short). If equity at a close is zero or below, the position is closed at that close with fees, the fill is marked `forced`, the fold reports `forced_closes`, and the replay trades no more.
- Not modelled: short-sale rejection or hard-to-borrow rates, buy-ins, margin interest on borrowed cash, rebates on short proceeds, dividends paid on shorts (prices are raw).

## Catalog multi-asset runs

`catalog_run.py` runs a rule over several symbols (OHLCV from Alpaca or Kraken via `catalog_data.py`) with the same fees, fills and borrow charge as `harness.py`, without changing it: one continuous run start..end, walk-forward only if the manifest sets `walk_forward`. Rules live in `catalog_rules.py`; each catalog folder's `multi*.json` holds the manifest.

`python catalog_report.py` runs every catalog folder that has a manifest (`manifest*.json` harness, `multi*.json`, `xs_manifest.json` via `strategies/xs/run_catalog.py`, `options_manifest*.json`), writes the standard report for each to `<folder>/results/<variant>/`, checks fills and the SPY drawdown, lists folders without a manifest as skipped, and regenerates `strategies/catalog/INDEX.md`.

Monte Carlo drawdown distributions: `python money.py mc <manifest>`, see docs/monte-carlo.md.
