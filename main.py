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
TIMEFRAME_MAP = {
    "5m": "5",
    "15m": "15",
    "1h": "60",
    "4h": "240",
    "1D": "1D"
}

NSE_SYMBOLS = [
    "NSE:RELIANCE",
    "NSE:TCS",
    "NSE:INFY",
    "NSE:HDFCBANK",
    "NSE:ICICIBANK",
    "NSE:LT",
    "NSE:SBIN",
    "NSE:AXISBANK",
    "NSE:ITC",
    "NSE:BAJFINANCE",
]

# ------------------ FETCH CANDLES ------------------
def fetch_history(symbol, resolution, bars=12):
    now = int(time.time())
    url = "https://tvc4.investing.com/1.1/1/chart/history"

    params = {
        "symbol": symbol,
        "resolution": resolution,
        "from": now - bars * 60 * int(resolution),
        "to": now
    }

    try:
        r = requests.get(url, params=params, timeout=5)
        data = r.json()
        if "c" not in data:
            return None

        return pd.DataFrame({
            "open": data["o"],
            "high": data["h"],
            "low": data["l"],
            "close": data["c"]
        })

    except:
        return None

# ------------------ REAL CRT ------------------
def detect_crt(df):
    if len(df) < 4:
        return None

    htf = df.iloc[-4:-2]
    ltf = df.iloc[-2:]

    range_high = htf["high"].max()
    range_low = htf["low"].min()

    last_close = ltf.iloc[-1]["close"]

    if last_close > range_high:
        return "Bullish CRT"

    if last_close < range_low:
        return "Bearish CRT"

    return None

# ------------------ BATCH SCAN ------------------
@app.get("/scan-batch")
def scan_batch(timeframe: str = Query("15m")):
    resolution = TIMEFRAME_MAP.get(timeframe)
    if not resolution:
        return []

    results = []

    for symbol in NSE_SYMBOLS:
        df = fetch_history(symbol, resolution)
        if df is None:
            continue

        crt = detect_crt(df)
        if not crt:
            continue

        results.append({
            "symbol": symbol,
            "timeframe": timeframe,
            "crt": crt,
            "chart": f"https://www.tradingview.com/chart/?symbol={symbol}"
        })

        time.sleep(0.3)  # 🚨 rate-limit safety

    return results

# ------------------ ROOT ------------------
@app.get("/")
def root():
    return {"status": "NSE CRT Batch Screener LIVE"}
