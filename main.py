from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import pandas as pd
import time

app = FastAPI(title="CRT Screener API")

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ CONFIG ------------------
TV_HISTORY_URL = "https://symbol-search.tradingview.com/symbol_search/"

TIMEFRAME_MAP = {
    "5m": "5",
    "15m": "15",
    "1h": "60",
    "4h": "240",
    "1D": "1D"
}

# ------------------ FETCH REAL CANDLES ------------------
def fetch_history(symbol, timeframe, bars=10):
    url = f"https://tvc4.investing.com/1.1/1/chart/history"
    params = {
        "symbol": symbol,
        "resolution": timeframe,
        "from": int(time.time()) - bars * 60 * int(timeframe),
        "to": int(time.time())
    }

    r = requests.get(url, params=params, timeout=10)
    data = r.json()

    if "c" not in data:
        return None

    df = pd.DataFrame({
        "open": data["o"],
        "high": data["h"],
        "low": data["l"],
        "close": data["c"]
    })

    return df

# ------------------ REAL CRT LOGIC ------------------
def detect_crt(df):
    if len(df) < 4:
        return None

    htf = df.iloc[-4:-2]
    ltf = df.iloc[-2:]

    range_high = htf["high"].max()
    range_low = htf["low"].min()

    last = ltf.iloc[-1]

    if last["close"] > range_high:
        return "Bullish CRT"

    if last["close"] < range_low:
        return "Bearish CRT"

    return None

# ------------------ API ------------------
@app.get("/scan")
def scan(
    symbol: str = Query(...),
    timeframe: str = Query("15m")
):
    tf = TIMEFRAME_MAP.get(timeframe)
    if not tf:
        return []

    df = fetch_history(symbol, tf)

    if df is None:
        return []

    crt = detect_crt(df)

    if not crt:
        return []

    return [{
        "symbol": symbol,
        "timeframe": timeframe,
        "crt": crt,
        "chart": f"https://www.tradingview.com/chart/?symbol={symbol}"
    }]

# ------------------ ROOT ------------------
@app.get("/")
def root():
    return {"status": "CRT Screener API LIVE"}
