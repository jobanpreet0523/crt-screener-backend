import pandas as pd


def analyze_liquidity(df: pd.DataFrame) -> dict:
    if df is None or len(df) < 5:
        return {"liquidity": "unknown"}

    highs = df["High"].tail(5)
    lows = df["Low"].tail(5)

    equal_highs = highs.max() - highs.min() < 0.1
    equal_lows = lows.max() - lows.min() < 0.1

    return {
        "equal_highs": bool(equal_highs),
        "equal_lows": bool(equal_lows),
        "liquidity_zone": (
            "buy_side" if equal_highs else
            "sell_side" if equal_lows else
            "none"
        )
    }
