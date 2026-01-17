from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Optional

# -------------------------------
# MOCK CRT LOGIC (replace later)
# -------------------------------
def scan_symbol(symbol: str, interval: str):
    """
    REALISTIC placeholder CRT logic.
    Replace this with your real CRT algorithm.
    """
    if symbol.upper().startswith("NIFTY"):
        return {
            "symbol": symbol,
            "timeframe": interval,
            "crt_type": "Bullish CRT",
            "status": "valid"
        }
    return None


def get_nse_symbols(limit: int = 50):
    """
    NSE universe (sample).
    You can later load from CSV or API.
    """
    symbols = [
        "NIFTY", "BANKNIFTY", "RELIANCE", "TCS", "INFY",
        "ICICIBANK", "HDFCBANK", "SBIN", "LT", "ITC",
        "AXISBANK", "KOTAKBANK", "BHARTIARTL", "HINDUNILVR"
    ]
    return symbols[:limit]


# -------------------------------
# APP SETUP
# -------------------------------
app = FastAPI(title="CRT Screener Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# HEALTH CHECK (IMPORTANT FOR RENDER)
# -------------------------------
@app.get("/")
def health():
    return {
        "status": "alive",
        "service": "CRT Screener Backend"
    }


# -------------------------------
# TIMEFRAME MAP
# -------------------------------
TF_MAP = {
    "5m": "5m",
    "15m": "15m",
    "1h": "1h",
    "daily": "1D",
    "weekly": "1W"
}


# -------------------------------
# SINGLE SYMBOL SCAN
# -------------------------------
@app.get("/scan")
def scan(
    symbol: str = Query(..., description="TradingView symbol"),
    timeframe: str = Query("daily", description="5m,15m,1h,daily")
):
    interval = TF_MAP.get(timeframe)

    if not interval:
        return {
            "error": "Invalid timeframe",
            "allowed": list(TF_MAP.keys())
        }

    result = scan_symbol(symbol, interval)

    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "found": bool(result),
        "result": result
    }


# -------------------------------
# NSE BATCH SCAN (50–200 SYMBOLS)
# -------------------------------
@app.get("/scan/nse")
def scan_nse(
    timeframe: str = "daily",
    limit: int = Query(50, ge=10, le=200)
):
    interval = TF_MAP.get(timeframe)

    if not interval:
        return {
            "error": "Invalid timeframe",
            "allowed": list(TF_MAP.keys())
        }

    symbols = get_nse_symbols(limit)
    results = []

    for symbol in symbols:
        res = scan_symbol(symbol, interval)
        if res:
            results.append(res)

    return {
        "market": "NSE",
        "timeframe": timeframe,
        "scanned": len(symbols),
        "found": len(results),
        "results": results
    }
