from __future__ import annotations

import random
from dataclasses import dataclass

from src.utils.time import now_utc_iso


@dataclass
class KalshiBookTick:
    ts: str
    kalshi_ticker: str
    best_yes_bid: int
    best_yes_ask: int
    best_no_bid: int
    best_no_ask: int
    depth_yes_top: int
    depth_no_top: int

    def to_dict(self) -> dict:
        mid = (self.best_yes_bid + self.best_yes_ask) / 2
        spread = self.best_yes_ask - self.best_yes_bid
        return {
            "ts": self.ts,
            "kalshi_ticker": self.kalshi_ticker,
            "best_yes_bid": self.best_yes_bid,
            "best_yes_ask": self.best_yes_ask,
            "best_no_bid": self.best_no_bid,
            "best_no_ask": self.best_no_ask,
            "mid_yes": mid,
            "spread_yes": spread,
            "depth_yes_top": self.depth_yes_top,
            "depth_no_top": self.depth_no_top,
        }


class MockKalshiWsClient:
    """Mock stream that emulates top-of-book updates for configured tickers."""

    def __init__(self, tickers: list[str]) -> None:
        self.tickers = tickers
        self._state = {t: 50 for t in tickers}

    def poll_ticks(self) -> list[dict]:
        ticks: list[dict] = []
        for ticker in self.tickers:
            center = self._state[ticker] + random.randint(-2, 2)
            center = max(5, min(95, center))
            self._state[ticker] = center
            spread = random.choice([2, 4, 6])
            bid = max(1, center - spread // 2)
            ask = min(99, center + spread // 2)
            ticks.append(
                KalshiBookTick(
                    ts=now_utc_iso(),
                    kalshi_ticker=ticker,
                    best_yes_bid=bid,
                    best_yes_ask=ask,
                    best_no_bid=max(1, 100 - ask),
                    best_no_ask=min(99, 100 - bid),
                    depth_yes_top=random.randint(20, 120),
                    depth_no_top=random.randint(20, 120),
                ).to_dict()
            )
        return ticks
