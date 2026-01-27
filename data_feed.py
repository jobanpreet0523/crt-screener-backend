import yfinance as yf
import pandas as pd


TIMEFRAME_MAP = {
    "1D": "1d",
    "1W": "1wk",
    "1M": "1mo",
    "15m": "15m",
    "5m": "5m"
}


def get_ohlc(symbol: str, timeframe: str) -> pd.DataFrame:
    interval = TIMEFRAME_MAP.get(timeframe)

    if not interval:
        return None

    try:
        data = yf.download(
            tickers=symbol,
            period="6mo",
            interval=interval,
            progress=False
        )

        if data.empty:
            return None

        data.reset_index(inplace=True)
        data = data[["Open", "High", "Low", "Close", "Volume"]]
        data.dropna(inplace=True)

        return data

    except Exception as e:
        print("Data feed error:", e)
        return None
