from __future__ import annotations

from dataclasses import dataclass


@dataclass
class RiskState:
    realized_pnl_day: float = 0.0
    open_positions: int = 0
    game_exposure: dict[str, int] | None = None

    def __post_init__(self) -> None:
        if self.game_exposure is None:
            self.game_exposure = {}
