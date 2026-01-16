def classify_crt(df):
    if df is None or len(df) < 3:
        return None

    c1 = df.iloc[-3]
    c2 = df.iloc[-2]
    c3 = df.iloc[-1]

    body1 = abs(c1["Close"] - c1["Open"])
    body2 = abs(c2["Close"] - c2["Open"])
    body3 = abs(c3["Close"] - c3["Open"])

    range1 = c1["High"] - c1["Low"]
    range2 = c2["High"] - c2["Low"]
    range3 = c3["High"] - c3["Low"]

    if body1 < range1 * 0.3 and body2 < range2 * 0.3:
        if body3 > range3 * 0.6:
            return "Bullish CRT" if c3["Close"] > c3["Open"] else "Bearish CRT"

    return None
