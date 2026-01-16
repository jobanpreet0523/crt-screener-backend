from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from scanner import scan_symbol
from universe import get_us_stocks

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {
        "status": "OK",
        "service": "CRT Screener Backend"
    }

@app.get("/scan")
def scan(tf: str = Query("daily")):

    tf_map = {
        "daily": "1d",
        "weekly": "1wk",
        "monthly": "1mo"
    }

    interval = tf_map.get(tf)
    if not interval:
        return {"error": "Invalid timeframe"}

    symbols = get_us_stocks()[:200]
    results = []

    for symbol in symbols:
        res = scan_symbol(symbol, interval)
        if res:
            results.append(res)

    return {
        "timeframe": tf,
        "total": len(results),
        "results": results
    }
