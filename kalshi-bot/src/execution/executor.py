from __future__ import annotations

import logging

logger = logging.getLogger(__name__)


class ShadowExecutor:
    """Signals-only mode: logs decisions without creating orders/fills."""

    def submit(self, signal: dict, approved: bool, reason: str) -> None:
        logger.info(
            "shadow_decision strategy=%s ticker=%s approved=%s reason=%s",
            signal.get("strategy_name"),
            signal.get("kalshi_ticker"),
            approved,
            reason,
        )
