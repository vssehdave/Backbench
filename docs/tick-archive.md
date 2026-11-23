# U.S. equity tick archive

The research downloader stores original Massive trade and top-of-book quote records for specified ticker symbols and completed UTC dates. Records preserve integer nanosecond SIP times, other timestamps as supplied, prices, sizes, exchanges, conditions and sequence identifiers. Use the SIP timestamp for consolidated-feed availability, then apply a separate dissemination delay to simulated decisions. The archive records the actual backfill time independently.

## Coverage and access

The vendor lists both datasets back to September 10, 2003, subject to listing history and subscription entitlements. Stocks Advanced lists all-history trades and quotes at USD 199 per month for individual use as checked November 22, 2026. Stocks Developer lists ten years of trades and excludes quotes. Check the intended use, endpoint and historical entitlements on the actual account. Ticker changes, mergers and delistings require a point-in-time identifier map for longitudinal research. Empty days alone establish neither a market holiday nor a complete history. Sources: [trades](https://massive.com/docs/rest/stocks/trades-quotes/trades), [quotes](https://massive.com/docs/rest/stocks/trades-quotes/quotes), [authentication](https://massive.com/docs/rest/quickstart).

## Run a one-session pilot

Set `MASSIVE_API_KEY` through a local secret manager or the process environment. Start with a licensed account and a data directory outside the repository.

```powershell
python tick_archive.py --symbols QQQ TQQQ --start 2016-01-04 --end 2016-01-05 --db D:/WalletData/2016-01.db
python -m unittest -v test_tick_archive
```

Both feeds are requested by default. Add `--feeds trades` for trades only. Supply the historical ticker spelling, including supported class suffixes such as BRK.B. The date range is half-open and includes extended-hours prints; apply an exchange calendar when building sessions. To acquire a year, use e.g. January 1, 2016 to January 1, 2017. Separate database paths by month or year to keep backups and storage manageable. Start with one day per symbol; measure compressed bytes per day, runtime, and quote volume before committing disk. For a market-wide history the provider's [daily bulk files](https://massive.com/docs/flat-files/stocks/overview) avoid repeating per-symbol REST requests.

Rerun the same command after interruption. Each page and its next cursor commit together. Completed partitions are skipped. Successful empty responses are tracked as zero rows. Failed requests remain incomplete. Status 401/403 requires checking the key and account access. Unknown cursor destinations are rejected. Bounded retries handle temporary HTTP and network errors. The cursor and request URLs exclude API keys. The archive treats completed days as snapshots; use a new archive path for a later vintage or correction audit.

## Inspect the data

```sql
SELECT symbol, kind, day, records, pages, next_url IS NULL AS complete
FROM partitions ORDER BY day, symbol, kind;
```

`pages.payload` is gzip-compressed JSON containing an array of original API records. To read a page, call `json.loads(gzip.decompress(payload))`. `pages.sha256` hashes the uncompressed UTF-8 JSON. Each page retains its provider request ID and receipt time. Preserve the raw layer; generate classified prints, corrected volume, as-of quotes, exchange sessions and Qlib features in separate derived datasets. The archive does not itself simulate fills or certify that the SIP feed has no gaps.
