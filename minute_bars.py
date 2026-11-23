"""Read the two VWAP TT minute-CSV layouts as regular-hours daily bars."""
import csv
import math
from datetime import date


def daily_from_minutes(path, symbol, start, end):
    bars = []
    counts = []
    previous_day = None
    previous_minute = None
    cached_date = None
    with open(path, newline="", encoding="utf-8-sig") as source:
        reader = csv.DictReader(source)
        fields = set(reader.fieldnames or ())
        stamp = "Datetime" if "Datetime" in fields else "Date"
        if not {stamp, "Open", "Close", "High", "Low", "Volume"} <= fields:
            raise ValueError("Expected a VWAP TT minute OHLCV file")
        for row in reader:
            if "Symbol" in row and row["Symbol"].upper() != symbol.upper():
                continue
            day_text, clock = row[stamp].split()
            if day_text != cached_date:
                if "/" in day_text:
                    month, day, year = map(int, day_text.split("/"))
                    day_value = date(year, month, day)
                else:
                    day_value = date.fromisoformat(day_text)
                cached_date = day_text
            if not start <= day_value < end:
                continue
            hour, minute, *seconds = map(int, clock.split(":"))
            if seconds and seconds != [0] or not (0 <= minute < 60 and 0 <= hour < 24):
                raise ValueError(f"Invalid minute stamp on line {reader.line_num}")
            time = hour * 60 + minute
            if not 570 <= time < 960:
                continue
            if previous_day and (day_value, time) <= (previous_day, previous_minute):
                raise ValueError(f"Duplicate or unordered minute on line {reader.line_num}")
            op, close = float(row["Open"]), float(row["Close"])
            if not all(math.isfinite(x) and x > 0 for x in (op, close)):
                raise ValueError(f"Unusable open or close on line {reader.line_num}")
            if day_value != previous_day:
                bars.append((day_value, op, close))
                counts.append([day_value.isoformat(), time, time, 1])
            else:
                bars[-1] = (day_value, bars[-1][1], close)
                counts[-1][2] = time
                counts[-1][3] += 1
            previous_day, previous_minute = day_value, time
    return bars, {
        "resolution": "daily from observed 09:30-15:59 Eastern minute bars",
        "symbol_source": "file column" if "Symbol" in fields else "user supplied",
        "session_count": len(bars),
        "sessions_under_390": [
            {"date": day, "first_minute": first, "last_minute": last, "observations": n}
            for day, first, last, n in counts if n < 390
        ],
    }
