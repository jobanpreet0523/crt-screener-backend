from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from scanner import scan_symbol
from universe import get_us_stocks

app = FastAPI(title="CRT Screener Backend")

# CORS (allow frontend access)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Timeframe map
TF_MAP = {
    "daily": "1d",
    "4h": "4h",
    "1h": "1h"
}

@app.get("/")
def health():
    return {
        "status": "OK",
        "service": "CRT Screener Backend"
    }

@app.get("/scan")
def scan(tf: str = Query("daily")):
    interval = TF_MAP.get(tf)

    if not interval:
        return {"error": "Invalid timeframe"}

    symbols = get_us_stocks()[:200]
    results = []

    for symbol in symbols:
        res = scan_symbol(symbol, interval)
        if res:
            results.append({
                "symbol": symbol,
                "crt": res,
                "timeframe": tf
            })

    return {
        "timeframe": tf,
        "total": len(results),
        "results": results
    }
