from fastapi import FastAPI
from enum import Enum
import yfinance as yf
import pandas as pd

app = FastAPI()

# ------------------------
# ENUM FOR TIMEFRAME
# ------------------------
class TimeFrame(str, Enum):
    daily = "daily"
    weekly = "weekly"
    monthly = "monthly"

# ------------------------
# HEALTH CHECK
# ------------------------
@app.get("/")
def root():
    return {"status": "ok", "message": "CRT Screener Backend Running"}

# ------------------------
# REGISTER
# ------------------------
@app.post("/register")
def register(user: dict):
    return {"msg": "User registered successfully", "username": user.get("username")}

# ------------------------
# LOGIN
# ------------------------
@app.post("/login")
def login(user: dict):
    return {"msg": "Login successful", "token": "dummy-token"}

# ------------------------
# CRT LOGIC
# ------------------------
def crt_signal(df: pd.DataFrame):
    prev = df.iloc[-2]
    curr = df.iloc[-1]

    mid = (prev["High"] + prev["Low"]) / 2

    if curr["Low"] < prev["Low"] and prev["Low"] < curr["Close"] < prev["High"] and curr["Close"] < mid:
        return "BUY CRT"

    if curr["High"] > prev["High"] and prev["Low"] < curr["Close"] < prev["High"] and curr["Close"] > mid:
        return "SELL CRT"

    return None

# ------------------------
# REAL SCAN ENDPOINT
# ------------------------
@app.get("/scan")
def scan(tf: TimeFrame = TimeFrame.daily):
    interval_map = {
        "daily": "1d",
        "weekly": "1wk",
        "monthly": "1mo"
    }

    tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "META"]
    results = []

    for t in tickers:
        df = yf.download(t, period="6mo", interval=interval_map[tf], progress=False)

        if len(df) < 10:
            continue

        signal = crt_signal(df)

        if signal:
            results.append({
                "symbol": t,
                "signal": signal,
                "close": round(df["Close"].iloc[-1], 2),
                "volume": int(df["Volume"].iloc[-1])
            })

    return {
        "timeframe": tf,
        "results": results
    }

