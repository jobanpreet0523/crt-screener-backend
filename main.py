from fastapi import FastAPI, Query, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

from universe import get_us_stocks
from crt_logic import classify_crt

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "CRT Screener Backend running"
    }

@app.get("/scan")
def scan(tf: str = Query("daily")):

    interval_map = {
        "daily": "1d",
        "weekly": "1wk",
        "monthly": "1mo"
    }

    if tf not in interval_map:
        raise HTTPException(status_code=400, detail="Invalid timeframe")

    interval = interval_map[tf]
    results = []

    symbols = get_us_stocks()[:50]  # SAFE LIMIT

    for symbol in symbols:
        try:
            df = yf.download(
                symbol,
                interval=interval,
                period="6mo",
                progress=False
            )

            if df.empty:
                continue

            crt_type = classify_crt(df)
            if crt_type:
                results.append({
                    "symbol": symbol,
                    "timeframe": tf,
                    "type": crt_type
                })

        except Exception:
            continue

    return {
        "total": len(results),
        "results": results
    }

@app.get("/debug")
def debug_one(symbol: str = "AAPL", tf: str = "daily"):
    interval_map = {
        "daily": "1d",
        "weekly": "1wk",
        "monthly": "1mo"
    }

    if tf not in interval_map:
        return {
            "error": "Invalid timeframe",
            "tf": tf
        }

    try:
        df = yf.download(
            symbol,
            interval=interval_map[tf],
            period="6mo",
            progress=False
        )

        if df is None or df.empty:
            return {
                "symbol": symbol,
                "error": "No price data returned"
            }

        crt = classify_crt(df)

        return {
            "symbol": symbol,
            "rows": len(df),
            "crt": crt
        }

    except Exception as e:
        return {
            "symbol": symbol,
            "exception": str(e)
        }
