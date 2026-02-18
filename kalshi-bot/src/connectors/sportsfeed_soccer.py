from __future__ import annotations

from dataclasses import dataclass

from src.utils.time import now_utc_iso


@dataclass
class MockSoccerState:
    game_id: str
    minute: int = 1
    stoppage_est: int = 4
    home_goals: int = 0
    away_goals: int = 0
    red_home: int = 0
    red_away: int = 0


class MockSoccerFeed:
    def __init__(self, game_ids: list[str]) -> None:
        self.states = {gid: MockSoccerState(game_id=gid) for gid in game_ids}

    def poll(self) -> list[dict]:
        out = []
        for state in self.states.values():
            state.minute = min(95, state.minute + 1)
            if state.minute in (30, 70):
                state.home_goals += 1
            out.append(
                {
                    "ts": now_utc_iso(),
                    "game_id": state.game_id,
                    "payload": {
                        "minute": state.minute,
                        "stoppage_est": state.stoppage_est,
                        "home_goals": state.home_goals,
                        "away_goals": state.away_goals,
                        "red_home": state.red_home,
                        "red_away": state.red_away,
                    },
                }
            )
        return out
