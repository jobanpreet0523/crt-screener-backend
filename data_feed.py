import yfinance as yf
import pandas as pd
from typing import Optional


TIMEFRAME_MAP = {
    "1D": "1d",
    "1W": "1wk",
    "1M": "1mo",
    "15m": "15m",
    "5m": "5m",
}


def get_ohlc(symbol: str, timeframe: str) -> Optional[pd.DataFrame]:
    interval = TIMEFRAME_MAP.get(timeframe)

    if interval is None:
        return None

    try:
        ticker = yf.Ticker(symbol)
        df = ticker.history(period="1y", interval=interval)

        if df.empty:
            return None

        df = df.reset_index()

        return df[["Open", "High", "Low", "Close", "Volume"]]

    except Exception as e:
        print(f"Data fetch error: {e}")
        return None
