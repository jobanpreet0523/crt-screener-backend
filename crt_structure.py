import pandas as pd


def analyze_crt(df: pd.DataFrame) -> dict:
    high = df["High"].max()
    low = df["Low"].min()
    close = df["Close"].iloc[-1]

    equilibrium = (high + low) / 2

    bias = "discount" if close < equilibrium else "premium"

    return {
        "range_high": round(high, 2),
        "range_low": round(low, 2),
        "equilibrium": round(equilibrium, 2),
        "current_close": round(close, 2),
        "bias": bias
    }
