import yfinance as yf

def get_ohlc(symbol):
    ticker = yf.Ticker(f"{symbol}.NS")
    df = ticker.history(period="5d", interval="1d")
    return df
