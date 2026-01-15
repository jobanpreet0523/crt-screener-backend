from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

# IMPORT PHASE 3 LOGIC
from phase3.universe import get_us_stocks
from phase3.crt_logic import is_crt

# -----------------------------
# CREATE APP (ONLY ONCE)
# -----------------------------
app = FastAPI()

# -----------------------------
# CORS
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("FASTAPI APP STARTING...")

# -----------------------------
# HEALTH CHECK
# -----------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "CRT Screener Backend is running",
        "docs": "/docs"
    }

# -----------------------------
# CRT SCANNER (PHASE 3)
# -----------------------------
@app.get("/scan")
def scan_crt(tf: str = Query("daily", description="daily, weekly, monthly")):

    interval_map = {
        "daily": "1d",
        "weekly": "1wk",
        "monthly": "1mo"
    }

    if tf not in interval_map:
        raise HTTPException(status_code=400, detail="Invalid timeframe")

    interval = interval_map[tf]

    symbols = get_us_stocks()[:200]   # SAFE LIMIT
    results = []

    for symbol in symbols:
        try:
            df = yf.download(
                symbol,
                period="6mo",
                interval=interval,
                progress=False
            )

            if df.empty:
                continue

            if is_crt(df):
                results.append({
                    "symbol": symbol,
                    "timeframe": tf,
                    "status": "CRT"
                })

        except:
            continue

    return {
        "total": len(results),
        "results": results
    }
