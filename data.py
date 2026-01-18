# data.py

def get_ohlc(symbol: str, timeframe: str = "1D", limit: int = 100):
    """
    Temporary dummy OHLC provider
    Replace later with NSE / broker / TV data
    """

    candles = []

    price = 100.0

    for _ in range(limit):
        open_ = price
        high = open_ * 1.01
        low = open_ * 0.99
        close = (high + low) / 2

        candles.append({
            "open": open_,
            "high": high,
            "low": low,
            "close": close
        })

        price = close

    return candles
