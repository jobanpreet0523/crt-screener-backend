# crt_scanner.py
# Complete CRT Scanner Engine

from typing import Dict, List
from sessions import get_session
from liquidity import detect_liquidity_sweep
from crt_structure import evaluate_crt_structure

Candle = Dict[str, float]


# ─────────────────────────────────────────────
# CRT SCAN RESULT
# ─────────────────────────────────────────────

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
    if session is None:
        return result

    result["session"] = session

    # 2️⃣ HTF Bias
    bias = evaluate_crt_structure(htf_candles)
    if bias not in ["BULLISH", "BEARISH"]:
        return result

    result["bias"] = bias

    # 3️⃣ Liquidity Sweep (LTF)
    liquidity = detect_liquidity_sweep(ltf_candles)
    if liquidity is None:
        return result

    result["liquidity"] = liquidity

    # Bias vs Liquidity Alignment
    if bias == "BULLISH" and liquidity != "SSL":
        return result
    if bias == "BEARISH" and liquidity != "BSL":
        return result

    # 4️⃣ LTF Structure Shift
    structure = evaluate_crt_structure(ltf_candles)
    if structure != bias:
        return result

    result["structure"] = structure

    # ─────────────────────────────────────────
    # 🎯 GRADING LOGIC
    # ─────────────────────────────────────────

    # Weak: Structure + Liquidity
    result["grade"] = "WEAK"

    # Valid: In London or NY
    if session in ["LONDON", "NEW_YORK"]:
        result["grade"] = "VALID"

    # A+ : NY Session + Full Alignment
    if (
        session == "NEW_YORK" and
        bias == structure
    ):
        result["grade"] = "A_PLUS"

    return result
