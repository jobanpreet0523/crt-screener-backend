# crt_structure.py
# CRT Screener – HTF / LTF Structure Engine
# Role: Define market bias and structural confirmation

from typing import List, Literal, Dict
from statistics import mean

Bias = Literal["bullish", "bearish", "neutral"]
Candle = Dict[str, float]


# ─────────────────────────────────────────────
# Utility Functions
# ─────────────────────────────────────────────

def candle_body(c: Candle) -> float:
    return abs(c["close"] - c["open"])


def candle_range(c: Candle) -> float:
    return c["high"] - c["low"]


def is_displacement(
    candles: List[Candle],
    index: int,
    factor: float = 1.5
) -> bool:
    """
    Detect displacement candle:
    body > factor × avg body of recent candles
    """
    if index < 5:
        return False

    recent_bodies = [
        candle_body(c) for c in candles[index-5:index]
    ]

    avg_body = mean(recent_bodies)
    return candle_body(candles[index]) > factor * avg_body


# ─────────────────────────────────────────────
# HTF STRUCTURE (BIAS ENGINE)
# ─────────────────────────────────────────────

def detect_htf_bias(
    candles: List[Candle]
) -> Bias:
    """
    Determine HTF market bias using structure + displacement
    """
    if len(candles) < 10:
        return "neutral"

    highs = [c["high"] for c in candles]
    lows = [c["low"] for c in candles]

    last = candles[-1]
    prev = candles[-2]

    # Bullish conditions
    bullish_structure = (
        last["high"] > max(highs[:-1]) and
        last["low"] > lows[-2] and
        is_displacement(candles, len(candles)-1) and
        last["close"] > prev["high"]
    )

    if bullish_structure:
        return "bullish"

    # Bearish conditions
    bearish_structure = (
        last["low"] < min(lows[:-1]) and
        last["high"] < highs[-2] and
        is_displacement(candles, len(candles)-1) and
        last["close"] < prev["low"]
    )

    if bearish_structure:
        return "bearish"

    return "neutral"


# ─────────────────────────────────────────────
# LTF STRUCTURE CONFIRMATION
# ─────────────────────────────────────────────

def confirm_ltf_structure(
    candles: List[Candle],
    htf_bias: Bias
) -> bool:
    """
    Confirm LTF structure aligns with HTF bias
    """
    if htf_bias == "neutral":
        return False

    if len(candles) < 6:
        return False

    last = candles[-1]
    prev = candles[-2]

    if htf_bias == "bullish":
        return (
            last["close"] > prev["high"] and
            candle_body(last) > candle_body(prev)
        )

    if htf_bias == "bearish":
        return (
            last["close"] < prev["low"] and
            candle_body(last) > candle_body(prev)
        )

    return False


# ─────────────────────────────────────────────
# CRT STRUCTURE WRAPPER
# ─────────────────────────────────────────────

def crt_structure_analysis(
    htf_candles: List[Candle],
    ltf_candles: List[Candle]
) -> Dict:
    """
    Full CRT structure analysis
    """
    bias = detect_htf_bias(htf_candles)
    ltf_confirmed = confirm_ltf_structure(ltf_candles, bias)

    return {
        "bias": bias,
        "ltf_confirmed": ltf_confirmed
    }
