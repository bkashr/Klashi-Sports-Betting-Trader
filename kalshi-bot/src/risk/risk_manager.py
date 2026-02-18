from __future__ import annotations

from src.risk.limits import RiskState
from src.strategies import reason_codes as rc


class RiskManager:
    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg
        self.state = RiskState()

    def vet(self, signal: dict) -> tuple[bool, str]:
        if signal["reason_code"].startswith("NO_TRADE"):
            return False, signal["reason_code"]

        risk_cfg = self.cfg
        if self.state.realized_pnl_day <= -risk_cfg["max_loss_day_usd"]:
            return False, rc.VETO_RISK_LIMIT_DAY

        if self.state.open_positions >= risk_cfg["max_open_positions"]:
            return False, rc.VETO_POSITION_LIMIT

        game_id = signal["game_id"]
        game_contracts = self.state.game_exposure.get(game_id, 0)
        if game_contracts >= risk_cfg["max_contracts_game"]:
            return False, rc.VETO_RISK_LIMIT_GAME

        return True, signal["reason_code"]
