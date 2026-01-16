def classify_crt(df):
    """
    Classifies a 3-candle CRT (Consolidation → Expansion) pattern.

    Rules:
    - Candle 1 & 2: small body (consolidation)
    - Candle 3: large body (expansion)
    - Direction based on Candle 3 close vs open

    Returns:
        "Bullish CRT" | "Bearish CRT" | None
    """

    if df is None or len(df) < 3:
        return None

    c1, c2, c3 = df.iloc[-3], df.iloc[-2], df.iloc[-1]

    def body(c):
        return abs(c["Close"] - c["Open"])

    def range_(c):
        return c["High"] - c["Low"]

    # Avoid division / zero range candles
    if range_(c1) == 0 or range_(c2) == 0 or range_(c3) == 0:
        return None

    # Consolidation candles (small bodies)
    is_consolidation = (
        body(c1) <= range_(c1) * 0.30 and
        body(c2) <= range_(c2) * 0.30
    )

    # Expansion candle (large body)
    is_expansion = body(c3) >= range_(c3) * 0.60

    if not (is_consolidation and is_expansion):
        return None

    return "Bullish CRT" if c3["Close"] > c3["Open"] else "Bearish CRT"
