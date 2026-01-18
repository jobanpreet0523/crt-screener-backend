import yfinance as yf

def get_ohlc(symbol, timeframe="15m", limit=200):
    ticker = yf.Ticker(symbol + ".NS")
    df = ticker.history(interval=timeframe, period="5d")
    return df.tail(limit)
