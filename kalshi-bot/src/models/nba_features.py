from __future__ import annotations


def score_diff(home_score: int, away_score: int) -> int:
    return home_score - away_score


def trailing_side(diff: int) -> str:
    if diff > 0:
        return "AWAY"
    if diff < 0:
        return "HOME"
    return "TIE"
