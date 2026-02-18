from __future__ import annotations

import math

from src.utils.math import poisson_cdf


def fair_over_probability(total_line: float, current_goals: int, t_remaining_min: float, pregame_total: float) -> float:
    mu_remaining = max(0.0, pregame_total * (t_remaining_min / 90.0))
    needed = math.floor(total_line - current_goals) + 1
    return 1.0 - poisson_cdf(needed - 1, mu_remaining)
