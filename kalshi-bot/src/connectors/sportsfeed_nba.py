from __future__ import annotations

from dataclasses import dataclass

from src.utils.time import now_utc_iso


@dataclass
class MockNbaState:
    game_id: str
    q: int = 1
    clock_sec: int = 720
    home_score: int = 0
    away_score: int = 0


class MockNbaFeed:
    def __init__(self, game_ids: list[str]) -> None:
        self.states = {gid: MockNbaState(game_id=gid) for gid in game_ids}

    def poll(self) -> list[dict]:
        out = []
        for state in self.states.values():
            state.clock_sec = max(0, state.clock_sec - 5)
            if state.clock_sec == 0 and state.q < 4:
                state.q += 1
                state.clock_sec = 720
            state.home_score += 1 if state.clock_sec % 20 == 0 else 0
            state.away_score += 1 if state.clock_sec % 23 == 0 else 0
            out.append(
                {
                    "ts": now_utc_iso(),
                    "game_id": state.game_id,
                    "payload": {
                        "q": state.q,
                        "clock_sec": state.clock_sec,
                        "home_score": state.home_score,
                        "away_score": state.away_score,
                    },
                }
            )
        return out
