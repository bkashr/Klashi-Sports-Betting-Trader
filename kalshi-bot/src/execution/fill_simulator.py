from __future__ import annotations

import math


def fee_cents(price_cents: int, contracts: int) -> int:
    p = price_cents / 100
    return int(math.ceil(0.07 * contracts * p * (1 - p)))
