def classify_crt(df):
    if df is None or len(df) < 20:
        return None

    df = df.dropna()

    # Last 3 candles
    c1 = df.iloc[-3]
    c2 = df.iloc[-2]
    c3 = df.iloc[-1]

    range1 = c1.High - c1.Low
    range2 = c2.High - c2.Low
    range3 = c3.High - c3.Low

    # ---------- CONFIRMED CRT ----------
    contraction = range3 < range2 < range1
    breakout = c3.Close > c2.High or c3.Close < c2.Low

    if contraction and breakout:
        return "CRT_CONFIRMED"

    # ---------- NEAR CRT ----------
    near_contraction = range3 < range2 and range2 < range1 * 1.1

    inside_bar = (
        c3.High <= c2.High and
        c3.Low >= c2.Low
    )

    if near_contraction or inside_bar:
        return "NEAR_CRT"

    return None
