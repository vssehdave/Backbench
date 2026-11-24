"""60-session time-series momentum: long when close / close 60 sessions ago - 1 is positive, else cash."""


def signal(history, lookback=60):
    """Return from `lookback` sessions before the latest close in `history`, or None with too little history."""
    if len(history) <= lookback:
        return None
    return history[-1] / history[-1 - lookback] - 1


def decide(history, level):
    """1 = fully long, 0 = cash, None = abstain (warmup). Share sizing is the runner's job (see run.py)."""
    s = signal(history, int(level))
    return None if s is None else int(s > 0)
