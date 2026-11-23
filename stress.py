"""Seeded daily-bar execution scenarios. Bounds express research assumptions."""
import random
from dataclasses import dataclass


@dataclass(frozen=True)
class StressConfig:
    max_delay_sessions: int = 0
    max_half_spread_bps: float = 0
    reject_probability: float = 0
    neighbour_steps: int = 0

    def __post_init__(self):
        if any(type(n) is not int or n < 0 for n in (self.max_delay_sessions, self.neighbour_steps)):
            raise ValueError("Delay and neighbour steps must be nonnegative integers")
        if not 0 <= self.max_half_spread_bps < 10000 or not 0 <= self.reject_probability <= 1:
            raise ValueError("Half spread must be in [0, 10000) bps and rejection probability in [0, 1]")

    def draw(self, seed, levels, selected):
        # Independent streams keep paired market innovations unchanged across scenario families.
        grid = sorted(set(levels))
        rank = grid.index(selected)
        candidates = grid[max(0, rank-self.neighbour_steps):rank+self.neighbour_steps+1]
        return PathStress(random.Random(f"{seed}:level").choice(candidates),
                          random.Random(f"{seed}:delay").randint(0, self.max_delay_sessions),
                          random.Random(f"{seed}:spread").uniform(0, self.max_half_spread_bps),
                          self.reject_probability)


@dataclass(frozen=True)
class PathStress:
    level: float
    delay_sessions: int
    half_spread_bps: float
    reject_probability: float


def max_drawdown(curve, opening_equity):
    peak = opening_equity
    worst = 0.
    for value in curve:
        peak = max(peak, value)
        worst = max(worst, (peak - value) / peak)
    return worst
