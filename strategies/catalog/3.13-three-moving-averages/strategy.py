"""Paper 3.13, long-only: long if MA(3) > MA(10) > MA(T); liquidate if MA(3) <= MA(10); else hold. level = T."""


def decide(history, level):
    t = int(level)
    a, b, c = (sum(history[-n:]) / n for n in (3, 10, t))
    if a > b > c:
        return int(5000 / history[0])
    return 0 if a <= b else None
