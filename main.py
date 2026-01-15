from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

from phase3.universe import get_us_stocks
from phase3.crt_logic import is_crt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/scan")
def scan_crt(tf: str = "daily"):

    interval_map = {
        "daily": "1d",
        "weekly": "1wk",
        "monthly": "1mo"
    }

    interval = interval_map.get(tf, "1d")

    symbols = get_us_stocks()

    results = []

    for symbol in symbols:
        df = yf.download(
            symbol,
            interval=interval,
            period="6mo",
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

    return {
        "total": len(results),
        "results": results
    }

