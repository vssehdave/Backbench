"""Deterministic controls. No investment hypotheses."""
def threshold(history, level):
    """Target ten whole shares above the threshold, otherwise cash."""
    return 10 if history[-1] > level else 0


def cash(history, level):
    return 0


class MeanThreshold:
    """Fitted control. The learned threshold is the training mean plus an offset."""

    @staticmethod
    def fit(rows, offset):
        return sum(close for _, _, close in rows) / len(rows) + offset

    decide = staticmethod(threshold)


def buy_and_hold(history, level):
    """Benchmark: hold the catalog's fixed position (half of 10,000 at the fold's first training close)."""
    return int(5000 / history[0])
