def classify_crt(df):
    """
    Detects CRT pattern:
    - Candle 1 & 2: consolidation (small bodies)
    - Candle 3: expansion (large body)
    """

    if df is None or len(df) < 3:
        return None

    try:
        c1 = df.iloc[-3]
        c2 = df.iloc[-2]
        c3 = df.iloc[-1]

        def body(c):
            return abs(c["Close"] - c["Open"])

        def rng(c):
            return c["High"] - c["Low"]

        # Avoid divide / bad data
        if rng(c1) == 0 or rng(c2) == 0 or rng(c3) == 0:
            return None

        # Consolidation candles
        if body(c1) < rng(c1) * 0.3 and body(c2) < rng(c2) * 0.3:
            # Expansion candle
            if body(c3) > rng(c3) * 0.6:
                return "Bullish CRT" if c3["Close"] > c3["Open"] else "Bearish CRT"

    except Exception:
        return None

    return None
