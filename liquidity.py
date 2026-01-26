# liquidity.py
# CRT Screener – Liquidity Sweep Detection
# Role: Detect BSL / SSL raids

from typing import List, Dict, Literal

Liquidity = Literal["BSL", "SSL", None]
Candle = Dict[str, float]


# ─────────────────────────────────────────────
# Swing Detection
# ─────────────────────────────────────────────

def is_swing_high(
    candles: List[Candle],
    index: int
) -> bool:
    if index < 2 or index >= len(candles) - 2:
        return False

    return (
        candles[index]["high"] > candles[index-1]["high"] and
        candles[index]["high"] > candles[index-2]["high"] and
        candles[index]["high"] > candles[index+1]["high"] and
        candles[index]["high"] > candles[index+2]["high"]
    )


def is_swing_low(
    candles: List[Candle],
    index: int
) -> bool:
    if index < 2 or index >= len(candles) - 2:
        return False

    return (
        candles[index]["low"] < candles[index-1]["low"] and
        candles[index]["low"] < candles[index-2]["low"] and
        candles[index]["low"] < candles[index+1]["low"] and
        candles[index]["low"] < candles[index+2]["low"]
    )


# ─────────────────────────────────────────────
# Liquidity Sweep Detection
# ─────────────────────────────────────────────

def detect_liquidity_sweep(
    candles: List[Candle]
) -> Liquidity:
    """
    Detect most recent liquidity sweep (BSL or SSL)
    """
    if len(candles) < 6:
        return None

    last = candles[-1]

    for i in range(len(candles) - 6, len(candles) - 1):

        # SSL – Sell-Side Liquidity
        if is_swing_low(candles, i):
            level = candles[i]["low"]

            if (
                last["low"] < level and
                last["close"] > level
            ):
                return "SSL"

        # BSL – Buy-Side Liquidity
        if is_swing_high(candles, i):
            level = candles[i]["high"]

            if (
                last["high"] > level and
                last["close"] < level
            ):
                return "BSL"

    return None
