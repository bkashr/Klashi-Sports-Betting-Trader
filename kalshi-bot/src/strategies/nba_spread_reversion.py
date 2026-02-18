from __future__ import annotations

from datetime import datetime, timezone

from src.models.nba_features import score_diff, trailing_side
from src.strategies import reason_codes as rc


class NbaSpreadReversionStrategy:
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

        payload = game_state["payload"]
        diff = score_diff(payload["home_score"], payload["away_score"])
        pregame_spread = abs(game.get("pregame_spread") or 999)
        run_mag = abs(diff)
        line = market["line_value"]
        snap = abs(line - diff) <= self.cfg["snap_delta"]
        q = payload.get("q", 4)
        clock_sec = payload.get("clock_sec", 0)
        time_remaining_min = ((4 - q) * 12) + clock_sec / 60

        spread = orderbook["spread_yes"]
        depth = min(orderbook["depth_yes_top"], orderbook["depth_no_top"])
        liquidity_ok = spread <= self.cfg.get("max_spread_cents", 6) and depth >= self.cfg.get("min_top_depth_contracts", 50)

        features = {
            "pregame_spread": pregame_spread,
            "score_diff": diff,
            "run_mag": run_mag,
            "time_remaining_min": time_remaining_min,
            "live_line": line,
            "snap": snap,
            "spread_cents": spread,
            "depth_top": depth,
        }

        if not liquidity_ok:
            return self._no_trade(ts, game["game_id"], market["kalshi_ticker"], rc.LIQUIDITY_FAIL, features)

        should_trade = (
            pregame_spread <= self.cfg["pregame_spread_max"]
            and run_mag >= self.cfg["run_threshold"]
            and snap
            and time_remaining_min >= self.cfg["min_time_remaining_min"]
        )
        if not should_trade:
            return self._no_trade(ts, game["game_id"], market["kalshi_ticker"], rc.NO_EDGE, features)

        trailing = trailing_side(diff)
        direction = "BUY_YES" if trailing == "HOME" else "BUY_NO"
        market_prob = orderbook["best_yes_ask"] / 100 if direction == "BUY_YES" else orderbook["best_no_ask"] / 100

        return {
            "ts": ts,
            "game_id": game["game_id"],
            "kalshi_ticker": market["kalshi_ticker"],
            "strategy_name": "nba_spread_reversion",
            "signal_strength": 1.0,
            "direction": direction,
            "fair_prob": None,
            "market_prob": market_prob,
            "edge": None,
            "reason_code": rc.TRADE_NBA_SIGNAL,
            "features": features,
        }

    @staticmethod
    def _no_trade(ts: str, game_id: str, ticker: str, reason: str, features: dict) -> dict:
        return {
            "ts": ts,
            "game_id": game_id,
            "kalshi_ticker": ticker,
            "strategy_name": "nba_spread_reversion",
            "reason_code": reason,
            "features": features,
        }
