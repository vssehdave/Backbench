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
