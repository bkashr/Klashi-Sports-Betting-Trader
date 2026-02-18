import unittest

from src.risk.risk_manager import RiskManager


class RiskRuleTests(unittest.TestCase):
    def test_risk_veto_day_loss(self) -> None:
        rm = RiskManager({"max_loss_day_usd": 25, "max_open_positions": 3, "max_contracts_game": 20})
        rm.state.realized_pnl_day = -26
        ok, reason = rm.vet({"reason_code": "TRADE: NBA_SIGNAL", "game_id": "g1"})
        self.assertFalse(ok)
        self.assertEqual(reason, "VETO: RISK_LIMIT_DAY")


if __name__ == "__main__":
    unittest.main()
