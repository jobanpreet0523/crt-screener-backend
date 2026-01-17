from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd

app = FastAPI(title="CRT Screener Backend")

# Allow frontend (Vercel / Localhost)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Utility: Detect CRT Pattern
# -----------------------------
def detect_crt(df: pd.DataFrame):
    """
    REAL CRT LOGIC
    Returns: Bullish CRT | Bearish CRT | None
    """

    if len(df) < 6:
        return None

    # Last 6 candles
    impulse = df.iloc[-6]
    consolidation = df.iloc[-5:-1]
    breakout = df.iloc[-1]

    impulse_range = impulse["High"] - impulse["Low"]
    avg_range = (df["High"] - df["Low"]).mean()

    # Impulse must be strong
    if impulse_range < avg_range * 1.5:
        return None

    cons_high = consolidation["High"].max()
    cons_low = consolidation["Low"].min()

    # Must stay inside impulse
    if cons_high > impulse["High"] or cons_low < impulse["Low"]:
        return None

    # -------- Bullish CRT --------
    if (
        impulse["Close"] > impulse["Open"]
        and breakout["Close"] > cons_high
    ):
        return "Bullish CRT"

    # -------- Bearish CRT --------
    if (
        impulse["Close"] < impulse["Open"]
        and breakout["Close"] < cons_low
    ):
        return "Bearish CRT"

    return None


# -----------------------------
# API Endpoint
# -----------------------------
@app.get("/scan")
def scan_crt(
    symbol: str = Query(..., example="AAPL"),
    timeframe: str = Query("1h", example="1h"),
):
    """
    Scans a symbol for CRT pattern
    """

    try:
        df = yf.download(
            tickers=symbol,
            period="60d",
            interval=timeframe,
            progress=False
        )

        if df.empty:
            return {"error": "No data found"}

        df.dropna(inplace=True)

        crt_result = detect_crt(df)

        last = df.iloc[-1]

        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "crt": crt_result or "No CRT",
            "price": round(float(last["Close"]), 2),
            "high": round(float(last["High"]), 2),
            "low": round(float(last["Low"]), 2),
        }

    except Exception as e:
        return {"error": str(e)}


# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def health():
    return {"status": "CRT Backend Running"}
