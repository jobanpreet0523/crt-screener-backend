# crt_scanner.py
# Complete CRT Scanner Engine

from typing import Dict, List
from sessions import get_session
from liquidity import detect_liquidity
from crt_structure import evaluate_crt_structure

Candle = Dict[str, float]


def scan_crt_setup(
    symbol: str,
    htf_candles: List[Candle],
    ltf_candles: List[Candle],
    timestamp_utc
) -> Dict:
    """
    Main CRT decision engine
    """

    result = {
        "symbol": symbol,
        "session": None,
        "bias": None,
        "liquidity": None,
        "structure": None,
        "grade": "NO_TRADE"
    }

    # 1️⃣ Session Filter
    session = get_session(timestamp_utc)
    if session == "OFF_SESSION":
        return result

    result["session"] = session

    # 2️⃣ HTF Bias
    bias, _ = evaluate_crt_structure(htf_candles, htf_candles)
    if bias not in ["BULLISH", "BEARISH"]:
        return result

    result["bias"] = bias

    # 3️⃣ Liquidity Sweep (LTF)
    liquidity = detect_liquidity(ltf_candles)
    if liquidity == "NO_LIQUIDITY":
        return result

    result["liquidity"] = liquidity

    # Bias vs Liquidity Alignment
    if bias == "BULLISH" and liquidity != "SSL_TAKEN":
        return result
    if bias == "BEARISH" and liquidity != "BSL_TAKEN":
        return result

    # 4️⃣ LTF Structure Shift
    structure, alignment = evaluate_crt_structure(htf_candles, ltf_candles)
    if alignment != "ALIGNED":
        return result

    result["structure"] = structure

    # ─────────────────────────────────────────
    # 🎯 GRADING LOGIC
    # ─────────────────────────────────────────

    result["grade"] = "WEAK"

    if session in ["LONDON", "NY"]:
        result["grade"] = "VALID"

    if session == "NY" and bias == structure:
        result["grade"] = "A_PLUS"

    return result
