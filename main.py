from fastapi import FastAPI
from universe import NSE_200
from data import get_ohlc
from scanner import is_doji

app = FastAPI()

@app.get("/screener/doji")
def doji_screener():
    results = []

    for symbol in NSE_200:
        ohlc = get_ohlc(symbol)
        if not ohlc:
            continue

        if is_doji(
            ohlc["open"],
            ohlc["high"],
            ohlc["low"],
            ohlc["close"]
        ):
            results.append({
                "symbol": symbol,
                **ohlc
            })

    return results
