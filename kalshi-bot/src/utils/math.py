from __future__ import annotations

import math


def poisson_cdf(k: int, lam: float) -> float:
    if k < 0:
        return 0.0
    if lam < 0:
        raise ValueError("lambda must be non-negative")
    total = 0.0
    for i in range(k + 1):
        total += math.exp(-lam) * lam**i / math.factorial(i)
    return min(max(total, 0.0), 1.0)
