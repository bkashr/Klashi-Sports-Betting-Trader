from __future__ import annotations

import json
from dataclasses import dataclass

from src.data.db import Database


@dataclass
class Repositories:
    db: Database

    def upsert_game(self, game: dict) -> None:
        self.db.execute(
            """
            INSERT INTO games(game_id,sport,league,home_team,away_team,start_time_utc,pregame_spread,pregame_total,status)
            VALUES(?,?,?,?,?,?,?,?,?)
            ON CONFLICT(game_id) DO UPDATE SET
              sport=excluded.sport, league=excluded.league, home_team=excluded.home_team,
              away_team=excluded.away_team, start_time_utc=excluded.start_time_utc,
              pregame_spread=excluded.pregame_spread, pregame_total=excluded.pregame_total,
              status=excluded.status, updated_at=CURRENT_TIMESTAMP
            """,
            (
                game["game_id"], game["sport"], game.get("league"), game.get("home_team"),
                game.get("away_team"), game.get("start_time_utc"), game.get("pregame_spread"),
                game.get("pregame_total"), game.get("status", "scheduled"),
            ),
        )

    def upsert_market_map(self, mapping: dict) -> None:
        self.db.execute(
            """
            INSERT INTO market_map(game_id,kalshi_ticker,market_type,line_value,side_convention_json)
            VALUES(?,?,?,?,?)
            ON CONFLICT(game_id,kalshi_ticker) DO UPDATE SET
                market_type=excluded.market_type,
                line_value=excluded.line_value,
                side_convention_json=excluded.side_convention_json
            """,
            (
                mapping["game_id"],
                mapping["kalshi_ticker"],
                mapping["market_type"],
                mapping["line_value"],
                json.dumps(mapping.get("side_convention", {})),
            ),
        )

    def insert_orderbook_tick(self, tick: dict) -> None:
        self.db.execute(
            """
            INSERT INTO orderbook_ticks(ts,kalshi_ticker,best_yes_bid,best_yes_ask,best_no_bid,best_no_ask,mid_yes,spread_yes,depth_yes_top,depth_no_top)
            VALUES(?,?,?,?,?,?,?,?,?,?)
            """,
            (
                tick["ts"], tick["kalshi_ticker"], tick.get("best_yes_bid"), tick.get("best_yes_ask"),
                tick.get("best_no_bid"), tick.get("best_no_ask"), tick.get("mid_yes"), tick.get("spread_yes"),
                tick.get("depth_yes_top"), tick.get("depth_no_top"),
            ),
        )

    def insert_game_state_tick(self, tick: dict) -> None:
        self.db.execute(
            "INSERT INTO game_state_ticks(ts,game_id,payload_json) VALUES(?,?,?)",
            (tick["ts"], tick["game_id"], json.dumps(tick["payload"])),
        )

    def insert_signal(self, signal: dict) -> None:
        self.db.execute(
            """
            INSERT INTO signals(ts,game_id,kalshi_ticker,strategy_name,signal_strength,direction,fair_prob,market_prob,edge,reason_code,features_json)
            VALUES(?,?,?,?,?,?,?,?,?,?,?)
            """,
            (
                signal["ts"], signal["game_id"], signal["kalshi_ticker"], signal["strategy_name"],
                signal.get("signal_strength"), signal.get("direction"), signal.get("fair_prob"),
                signal.get("market_prob"), signal.get("edge"), signal["reason_code"],
                json.dumps(signal.get("features", {})),
            ),
        )

    def get_latest_orderbook(self, ticker: str) -> dict | None:
        rows = self.db.query(
            "SELECT * FROM orderbook_ticks WHERE kalshi_ticker=? ORDER BY ts DESC LIMIT 1",
            (ticker,),
        )
        return dict(rows[0]) if rows else None

    def get_latest_game_state(self, game_id: str) -> dict | None:
        rows = self.db.query(
            "SELECT * FROM game_state_ticks WHERE game_id=? ORDER BY ts DESC LIMIT 1",
            (game_id,),
        )
        if not rows:
            return None
        row = dict(rows[0])
        row["payload"] = json.loads(row["payload_json"])
        return row

    def get_market_map_for_game(self, game_id: str) -> list[dict]:
        rows = self.db.query("SELECT * FROM market_map WHERE game_id=?", (game_id,))
        out = []
        for r in rows:
            d = dict(r)
            d["side_convention"] = json.loads(d["side_convention_json"])
            out.append(d)
        return out

    def get_games(self) -> list[dict]:
        return [dict(r) for r in self.db.query("SELECT * FROM games")]
