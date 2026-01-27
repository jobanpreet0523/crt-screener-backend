import pandas as pd


def analyze_crt(df: pd.DataFrame) -> dict:
    if df is None or len(df) < 3:
        return {"valid": False}

    high = df["High"].iloc[-1]
    low = df["Low"].iloc[-1]
    prev_high = df["High"].iloc[-2]
    prev_low = df["Low"].iloc[-2]

    bullish_crt = low > prev_low and high > prev_high
    bearish_crt = high < prev_high and low < prev_low

    return {
        "valid": bullish_crt or bearish_crt,
        "bias": "bullish" if bullish_crt else "bearish" if bearish_crt else "neutral",
        "range_high": float(high),
        "range_low": float(low),
    }
