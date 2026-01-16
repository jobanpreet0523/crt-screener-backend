def classify_crt(df):
    if len(df) < 3:
        return None

    c1, c2, c3 = df.iloc[-3], df.iloc[-2], df.iloc[-1]

    def body(c):
        return abs(c["Close"] - c["Open"])

    def candle_range(c):
        return c["High"] - c["Low"]

    is_consolidation = (
        body(c1) < candle_range(c1) * 0.3 and
        body(c2) < candle_range(c2) * 0.3
    )

    is_expansion = body(c3) > candle_range(c3) * 0.6

    if is_consolidation and is_expansion:
        return "Bullish CRT" if c3["Close"] > c3["Open"] else "Bearish CRT"

    return None
