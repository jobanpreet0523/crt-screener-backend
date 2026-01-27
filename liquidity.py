import pandas as pd


def analyze_liquidity(df: pd.DataFrame) -> dict:
    highs = df["High"]
    lows = df["Low"]

    buyside_liquidity = highs[:-1].max()
    sellside_liquidity = lows[:-1].min()

    last_high = highs.iloc[-1]
    last_low = lows.iloc[-1]

    swept_buyside = last_high > buyside_liquidity
    swept_sellside = last_low < sellside_liquidity

    return {
        "buyside_level": round(buyside_liquidity, 2),
        "sellside_level": round(sellside_liquidity, 2),
        "buyside_swept": swept_buyside,
        "sellside_swept": swept_sellside
    }
