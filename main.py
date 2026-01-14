from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

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
