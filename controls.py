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
