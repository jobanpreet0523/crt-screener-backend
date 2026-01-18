# data.py

import yfinance as yf
import pandas as pd


def get_ohlc(symbol: str, interval="1d", period="6mo"):
    """
    Fetch OHLC data from Yahoo Finance for NSE stocks
    """

    ticker = symbol + ".NS"   # NSE suffix
    df = yf.download(
        ticker,
        interval=interval,
        period=period,
        progress=False
    )

    if df.empty:
        return None

    df = df.reset_index()

    return df[["Date", "Open", "High", "Low", "Close", "Volume"]]
