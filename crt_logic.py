def classify_crt(symbol: str, interval: str):
    """
    Return 'Bullish', 'Bearish', or None
    """

    # TEMP SAFE LOGIC (replace later with real CRT)
    if symbol.endswith("USD"):
        return "Bullish"

    return None
