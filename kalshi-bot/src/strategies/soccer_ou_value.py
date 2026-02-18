from __future__ import annotations

from datetime import datetime, timezone

from src.models.soccer_poisson import fair_over_probability
from src.strategies import reason_codes as rc


class SoccerOuValueStrategy:
    def __init__(self, cfg: dict) -> None:
        self.cfg = cfg

    def evaluate(self, game: dict, market: dict, game_state: dict | None, orderbook: dict | None) -> dict:
        ts = datetime.now(timezone.utc).isoformat()
        if not market:
            return self._no_trade(ts, game["game_id"], "", rc.MISSING_MAPPING, {})
        if not game_state:
            return self._no_trade(ts, game["game_id"], market["kalshi_ticker"], rc.STALE_GAME_STATE, {})
        if not orderbook:
            return self._no_trade(ts, game["game_id"], market["kalshi_ticker"], rc.STALE_ORDERBOOK, {})

        p = game_state["payload"]
        if self.cfg.get("red_card_filter", True) and (p.get("red_home", 0) + p.get("red_away", 0)) > 0:
            return self._no_trade(ts, game["game_id"], market["kalshi_ticker"], rc.NO_EDGE, {"red_cards": True})

        spread = orderbook["spread_yes"]
        depth = min(orderbook["depth_yes_top"], orderbook["depth_no_top"])
        liquidity_ok = spread <= self.cfg.get("max_spread_cents", 6) and depth >= self.cfg.get("min_top_depth_contracts", 50)
        if not liquidity_ok:
            return self._no_trade(ts, game["game_id"], market["kalshi_ticker"], rc.LIQUIDITY_FAIL, {"spread": spread, "depth": depth})

        pregame_total = game.get("pregame_total")
        if pregame_total is None:
            return self._no_trade(ts, game["game_id"], market["kalshi_ticker"], rc.NO_EDGE, {"missing_pregame_total": True})

        goals = p.get("home_goals", 0) + p.get("away_goals", 0)
        t_remaining = max(0, 90 - p.get("minute", 90) + p.get("stoppage_est", 0))
        line = market["line_value"]

        p_fair = fair_over_probability(line, goals, t_remaining, pregame_total)
        p_market_yes = orderbook["best_yes_ask"] / 100
        p_market_no = orderbook["best_no_ask"] / 100

        edge_yes = p_fair - p_market_yes
        edge_no = (1 - p_fair) - p_market_no

        direction = None
        edge = None
        market_prob = None
        if edge_yes >= self.cfg["edge_min"]:
            direction, edge, market_prob = "BUY_YES", edge_yes, p_market_yes
        elif edge_no >= self.cfg["edge_min"]:
            direction, edge, market_prob = "BUY_NO", edge_no, p_market_no

        features = {
            "goals": goals,
            "line": line,
            "t_remaining": t_remaining,
            "p_fair": p_fair,
            "edge_yes": edge_yes,
            "edge_no": edge_no,
        }

        if direction is None:
            return self._no_trade(ts, game["game_id"], market["kalshi_ticker"], rc.NO_EDGE, features)

        net_edge_estimate = edge - (spread / 100)
        features["net_edge_estimate"] = net_edge_estimate
        if net_edge_estimate < self.cfg["net_edge_min"]:
            return self._no_trade(ts, game["game_id"], market["kalshi_ticker"], rc.NO_EDGE, features)

        return {
            "ts": ts,
            "game_id": game["game_id"],
            "kalshi_ticker": market["kalshi_ticker"],
            "strategy_name": "soccer_ou_value",
            "signal_strength": edge,
            "direction": direction,
            "fair_prob": p_fair,
            "market_prob": market_prob,
            "edge": edge,
            "reason_code": rc.TRADE_SOCCER_VALUE,
            "features": features,
        }

    @staticmethod
    def _no_trade(ts: str, game_id: str, ticker: str, reason: str, features: dict) -> dict:
        return {
            "ts": ts,
            "game_id": game_id,
            "kalshi_ticker": ticker,
            "strategy_name": "soccer_ou_value",
            "reason_code": reason,
            "features": features,
        }
