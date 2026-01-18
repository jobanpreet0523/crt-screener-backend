def detect_bullish_crt(df):
    high = df["High"]
    low = df["Low"]

    if low.iloc[-2] < low.iloc[-3] and df["Close"].iloc[-1] > high.iloc[-2]:
        return {
            "direction": "BUY",
            "crt_type": "Bullish CRT",
            "entry": high.iloc[-2],
            "sl": low.iloc[-2]
        }
    return None
