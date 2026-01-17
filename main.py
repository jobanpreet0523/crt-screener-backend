from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import yfinance as yf

app = FastAPI()

# Allow React / TradingView frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# SYMBOL UNIVERSE (EDIT HERE)
# -----------------------------
SYMBOLS = [
    "ES=F",     # S&P 500 Futures
    "NQ=F",     # Nasdaq Futures
    "YM=F",     # Dow Futures
    "GC=F",     # Gold
    "CL=F",     # Crude Oil
]

# -----------------------------
# CRT LOGIC
# -----------------------------
def detect_crt(df: pd.DataFrame):
    """
    CRT MODEL:
    - Consolidation (small range)
    - Manipulation (liquidity sweep)
    - Expansion (strong close)
    """

    if len(df) < 20:
        return None

    recent = df.tail(20)

    high = recent["High"].max()
    low = recent["Low"].min()
    range_size = high - low

    last = recent.iloc[-1]
    prev = recent.iloc[-2]

    # Consolidation check
    avg_range = (recent["High"] - recent["Low"]).mean()
    is_consolidation = range_size < avg_range * 2

    # Manipulation
    sweep_high = last["High"] > high * 0.999 and last["Close"] < prev["High"]
    sweep_low = last["Low"] < low * 1.001 and last["Close"] > prev["Low"]

    # Expansion
    bullish_expansion = last["Close"] > last["Open"] and last["Close"] > prev["High"]
    bearish_expansion = last["Close"] < last["Open"] and last["Close"] < prev["Low"]

    if is_consolidation and sweep_low and bullish_expansion:
        return "BULLISH_CRT"

    if is_consolidation and sweep_high and bearish_expansion:
        return "BEARISH_CRT"

    return None


# -----------------------------
# API ENDPOINT
# -----------------------------
@app.get("/scan")
def scan_market():
    results = []

    for symbol in SYMBOLS:
        try:
            df = yf.download(
                symbol,
                interval="5m",
                period="5d",
                progress=False
            )

            if df.empty:
                continue

            signal = detect_crt(df)

            if signal:
                results.append({
                    "symbol": symbol,
                    "signal": signal,
                    "price": float(df.iloc[-1]["Close"])
                })

        except Exception as e:
            print(f"Error scanning {symbol}: {e}")

    return {
        "count": len(results),
        "results": results
    }


# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
def root():
    return {"status": "CRT Screener Live"}
