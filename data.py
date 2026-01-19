import yfinance as yf

def get_ohlc(symbol):
    ticker = yf.Ticker(symbol + ".NS")
    df = ticker.history(period="5d")
    if df.empty:
        return None
    last = df.iloc[-1]
    return {
        "open": round(last["Open"], 2),
        "high": round(last["High"], 2),
        "low": round(last["Low"], 2),
        "close": round(last["Close"], 2)
    }
