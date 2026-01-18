# crt_logic.py

def detect_crt(candles):
    """
    candles: list of OHLC candles
    returns: dict | None
    """

    if not candles or len(candles) < 3:
        return None

    prev = candles[-3]
    base = candles[-2]
    curr = candles[-1]

    # Basic CRT logic (you can enhance later)
    if (
        base["low"] < prev["low"]
        and curr["close"] > base["high"]
    ):
        return {
            "type": "BULLISH_CRT",
            "base_high": base["high"],
            "base_low": base["low"]
        }

    if (
        base["high"] > prev["high"]
        and curr["close"] < base["low"]
    ):
        return {
            "type": "BEARISH_CRT",
            "base_high": base["high"],
            "base_low": base["low"]
        }

    return None
