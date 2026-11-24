"""Fetch EDGAR facts for every ticker in the cached S&P 500 panel. Usage: python fetch_edgar.py"""
from datetime import date
import edgar
import xs_data

panel = xs_data.build_panel(date(2015, 1, 1), date(2026, 11, 1))
cik = edgar.ticker_map()
symbols = sorted(panel.adj)
missing = [s for s in symbols if s not in cik]
print(len(symbols), "symbols,", len(missing), "without CIK:", missing, flush=True)
for n, s in enumerate(symbols):
    if s in cik:
        edgar.company(cik[s])
    if n % 50 == 0:
        print(n, flush=True)
print("done")
