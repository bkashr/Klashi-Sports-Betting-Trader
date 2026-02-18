import unittest

from src.strategies.nba_spread_reversion import NbaSpreadReversionStrategy


class NbaSignalTests(unittest.TestCase):
    def test_nba_signal_no_trade_when_no_edge(self) -> None:
        s = NbaSpreadReversionStrategy(
            {
                "pregame_spread_max": 4.5,
                "run_threshold": 6,
                "snap_delta": 1.0,
                "min_time_remaining_min": 12,
                "max_spread_cents": 6,
                "min_top_depth_contracts": 50,
            }
        )
        game = {"game_id": "g1", "pregame_spread": -2.0}
        market = {"kalshi_ticker": "T", "line_value": -2.5}
        game_state = {"payload": {"q": 2, "clock_sec": 500, "home_score": 20, "away_score": 20}}
        orderbook = {"spread_yes": 2, "depth_yes_top": 100, "depth_no_top": 100, "best_yes_ask": 52, "best_no_ask": 48}
        sig = s.evaluate(game, market, game_state, orderbook)
        self.assertTrue(sig["reason_code"].startswith("NO_TRADE"))


if __name__ == "__main__":
    unittest.main()
