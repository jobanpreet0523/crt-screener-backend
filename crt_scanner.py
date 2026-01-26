# crt_scanner.py
# Complete CRT Scanner Engine (Aligned with backend modules)

from typing import Dict, List
from datetime import datetime

from sessions import get_current_session, allow_a_plus
from liquidity import detect_liquidity_sweep
from crt_structure import crt_structure_analysis

Candle = Dict[str, float]


def scan_crt_setup(
    symbol: str,
    htf_candles: List[Candle],
    ltf_candles: List[Candle],
    timestamp_utc: datetime
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
    session = get_current_session(timestamp_utc)
    if session == "Off":
        return result

    result["session"] = session

    # 2️⃣ HTF / LTF CRT Structure
    structure = crt_structure_analysis(
        htf_candles=htf_candles,
        ltf_candles=ltf_candles
    )

    bias = structure["bias"]
    ltf_confirmed = structure["ltf_confirmed"]

    if bias not in ("bullish", "bearish"):
        return result

    result["bias"] = bias

    # 3️⃣ Liquidity Sweep (LTF)
    liquidity = detect_liquidity_sweep(ltf_candles)
    if liquidity is None:
        return result

    result["liquidity"] = liquidity

    # Bias ↔ Liquidity alignment
    if bias == "bullish" and liquidity != "SSL":
        return result

    if bias == "bearish" and liquidity != "BSL":
        return result

    # 4️⃣ LTF Structure Confirmation
    if not ltf_confirmed:
        return result

    result["structure"] = "CONFIRMED"

    # ─────────────────────────────────────
    # 🎯 GRADING LOGIC
    # ─────────────────────────────────────

    result["grade"] = "WEAK"

    if session in ("London", "NewYork"):
        result["grade"] = "VALID"

    if allow_a_plus(session, timestamp_utc):
        result["grade"] = "A_PLUS"

    return result
