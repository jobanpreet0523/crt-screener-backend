from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import requests
import pandas as pd

app = FastAPI(title="CRT Screener API")

# ------------------ CORS ------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # lock later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------ CONFIG ------------------
TV_BASE_URL = "https://scanner.tradingview.com/india/scan"

TIMEFRAME_MAP = {
    "5m": "5",
    "15m": "15",
    "1h": "60",
    "4h": "240",
    "1D": "1D"
}

# ------------------ CRT LOGIC ------------------
def detect_crt(df: pd.DataFrame):
    """
    CRT Model:
    - Higher timeframe structure intact
    - Lower timeframe candle closes back inside range
    """

    if len(df) < 3:
        return None

    prev = df.iloc[-2]
    curr = df.iloc[-1]

    # Bullish CRT
    if curr["close"] > prev["high"]:
        return "Bullish CRT"

    # Bearish CRT
    if curr["close"] < prev["low"]:
        return "Bearish CRT"

    return None

# ------------------ FETCH DATA ------------------
def fetch_ohlc(symbol: str, timeframe: str):
    payload = {
        "symbols": {
            "tickers": [symbol],
            "query": {"types": []}
        },
        "columns": [
            "open",
            "high",
            "low",
            "close",
            "volume"
        ]
    }

    res = requests.post(TV_BASE_URL, json=payload, timeout=10)

    if res.status_code != 200:
        return None

    data = res.json()["data"]

    if not data:
        return None

    values = data[0]["d"]

    df = pd.DataFrame(
        [values],
        columns=["open", "high", "low", "close", "volume"]
    )

    return df

# ------------------ API ENDPOINT ------------------
@app.get("/scan")
def scan(
    symbol: str = Query(..., description="TradingView symbol"),
    timeframe: str = Query("15m", description="Timeframe")
):
    tf = TIMEFRAME_MAP.get(timeframe)

    if not tf:
        return {"error": "Invalid timeframe"}

    df = fetch_ohlc(symbol, tf)

    if df is None:
        return {"error": "No data received"}

    crt_signal = detect_crt(df)

    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "crt": crt_signal,
        "status": "OK"
    }

# ------------------ ROOT ------------------
@app.get("/")
def root():
    return {"status": "CRT Screener API is LIVE"}
