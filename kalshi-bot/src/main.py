from __future__ import annotations

import argparse
import logging
import time
from pathlib import Path

import json

from src.connectors.kalshi_ws import MockKalshiWsClient
from src.connectors.sportsfeed_nba import MockNbaFeed
from src.connectors.sportsfeed_soccer import MockSoccerFeed
from src.data.db import Database, init_schema
from src.data.repositories import Repositories
from src.execution.executor import ShadowExecutor
from src.risk.risk_manager import RiskManager
from src.strategies.nba_spread_reversion import NbaSpreadReversionStrategy
from src.strategies.soccer_ou_value import SoccerOuValueStrategy
from src.utils.logging import setup_logging

logger = logging.getLogger(__name__)


def load_yaml(path: str) -> dict:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def bootstrap_games(repos: Repositories) -> None:
    repos.upsert_game(
        {
            "game_id": "nba_game_1",
            "sport": "nba",
            "league": "NBA",
            "home_team": "HOME",
            "away_team": "AWAY",
            "start_time_utc": "2026-01-01T00:00:00Z",
            "pregame_spread": -2.0,
            "status": "live",
        }
    )
    repos.upsert_game(
        {
            "game_id": "soccer_match_1",
            "sport": "soccer",
            "league": "EPL",
            "home_team": "A",
            "away_team": "B",
            "start_time_utc": "2026-01-01T00:00:00Z",
            "pregame_total": 2.5,
            "status": "live",
        }
    )


def main(config_path: str) -> None:
    setup_logging()
    cfg = load_yaml(config_path)
    markets_cfg = load_yaml(str(Path(config_path).parent / "markets.yaml"))

    db = Database(cfg["database"]["path"])
    init_schema(db, str(Path(__file__).parent / "data" / "schema.sql"))
    repos = Repositories(db)

    bootstrap_games(repos)
    for mapping in markets_cfg.get("mappings", []):
        repos.upsert_market_map(mapping)

    games = repos.get_games()
    tickers = [m["kalshi_ticker"] for g in games for m in repos.get_market_map_for_game(g["game_id"])]
    ws = MockKalshiWsClient(tickers)
    nba_feed = MockNbaFeed([g["game_id"] for g in games if g["sport"] == "nba"])
    soccer_feed = MockSoccerFeed([g["game_id"] for g in games if g["sport"] == "soccer"])

    nba_strategy = NbaSpreadReversionStrategy(
        {**cfg["strategy"]["nba"], **cfg["liquidity"]}
    )
    soccer_strategy = SoccerOuValueStrategy(
        {**cfg["strategy"]["soccer"], **cfg["liquidity"]}
    )
    risk = RiskManager(cfg["risk"])
    executor = ShadowExecutor()

    iterations = cfg["runtime"].get("loop_iterations", 20)
    eval_sleep = cfg["runtime"].get("evaluation_interval_seconds", 5)

    for i in range(iterations):
        for tick in ws.poll_ticks():
            repos.insert_orderbook_tick(tick)

        for tick in nba_feed.poll() + soccer_feed.poll():
            repos.insert_game_state_tick(tick)

        for game in repos.get_games():
            markets = repos.get_market_map_for_game(game["game_id"])
            market = markets[0] if markets else None
            orderbook = repos.get_latest_orderbook(market["kalshi_ticker"]) if market else None
            gstate = repos.get_latest_game_state(game["game_id"])

            if game["sport"] == "nba":
                signal = nba_strategy.evaluate(game, market, gstate, orderbook)
            else:
                signal = soccer_strategy.evaluate(game, market, gstate, orderbook)

            repos.insert_signal(signal)
            approved, reason = risk.vet(signal)
            executor.submit(signal, approved, reason)

        logger.info("loop_iteration=%s complete", i + 1)
        time.sleep(eval_sleep)

    db.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config/settings.yaml")
    args = parser.parse_args()
    main(args.config)
