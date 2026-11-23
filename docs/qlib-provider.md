# Qlib daily provider acceptance

Use CPython 3.11 x64 and install the pinned Qlib release in an isolated environment. From the repository root on Windows:

```powershell
py -3.11 -m venv .venv
.\.venv\Scripts\python -m pip install -r requirements-qlib.txt
.\.venv\Scripts\python test_qlib_provider.py -v
```

The standalone acceptance command fails when Qlib is missing. General unittest discovery reports an explicit skip so the standard-library harness can still be tested.

The test writes a two-year synthetic daily binary provider to a temporary directory, calls the actual Qlib adapter, and compares every returned date and price with its source. It checks inclusive endpoint clipping and compares full walk-forward reports, including orders, fees and seeded scenarios, with a direct replay of the same observations. It requires no market data or API keys.

This fixture only exercises daily ingestion. Its weekday calendar includes exchange holidays. Real-world session completeness, publication delays, raw and adjusted price conventions, and tick-to-bar aggregation require a separate vendor-data acceptance test. The Qlib package version is pinned; transitive dependencies are resolved by pip. [Qlib release files](https://pypi.org/project/pyqlib/0.9.7/#files)
