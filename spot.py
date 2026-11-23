"""Assumed costs and lot sizing for 24/7 USD spot markets, plus a synthetic UTC fixture."""
import math
from dataclasses import dataclass
from datetime import date, timedelta


@dataclass(frozen=True)
class Spot:
    fee_bps: float
    lot_size: float
    min_notional_usd: float

    def __post_init__(self):
        values = (self.fee_bps, self.lot_size, self.min_notional_usd)
        if not all(math.isfinite(v) and v >= 0 for v in values) or self.lot_size == 0:
            raise ValueError("Spot fee and minimum must be finite and nonnegative; lot size must be positive")

    @property
    def profile(self):
        return f"spot-{self.fee_bps}bps-lot{self.lot_size}-min{self.min_notional_usd}usd"

    def commission(self, order_value):
        return abs(order_value) * self.fee_bps / 10000


def spot_fixture():
    """One bar per UTC calendar date, weekends included."""
    rows = []
    day = date(2022, 1, 1)
    while day < date(2024, 1, 1):
        i = len(rows)
        rows.append((day, 100 + 5 * math.sin(i / 12), 100 + 5 * math.sin((i + 0.5) / 12)))
        day += timedelta(days=1)
    return rows
