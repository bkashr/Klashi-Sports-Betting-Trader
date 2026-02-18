from __future__ import annotations


class KalshiRestClient:
    """Placeholder REST client for future live mode order routing."""

    def __init__(self, base_url: str | None = None) -> None:
        self.base_url = base_url or "https://api.elections.kalshi.com"

    def health(self) -> dict:
        return {"ok": True, "base_url": self.base_url}
