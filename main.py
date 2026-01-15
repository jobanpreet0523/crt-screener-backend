from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
@app.get("/scan")
def scan_crt(tf: str = "daily"):
    interval_map = {
        "daily": "1d",
        "weekly": "1wk",
        "monthly": "1mo"
    }

    interval = interval_map.get(tf, "1d")

    symbols = get_us_stocks()[:200]  # start small (SAFE)

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

app = FastAPI()
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # allow all (for testing)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("FASTAPI APP STARTING...")
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "CRT Screener Backend is running",
        "docs": "/docs"
    }
@app.get("/scan")
def scan(tf: str = Query(..., description="daily, weekly, monthly")):

    tf_map = {
        "daily": "1d",
        "weekly": "1wk",
        "monthly": "1mo"
    }

    if tf not in tf_map:
        raise HTTPException(status_code=400, detail="Invalid timeframe")

    data = yf.download(
        tickers="AAPL MSFT TSLA",
        interval=tf_map[tf],
        period="6mo",
        progress=False
    )

    return {
        "status": "success",
        "timeframe": tf
    }
