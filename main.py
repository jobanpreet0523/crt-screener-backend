from fastapi import FastAPI
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
def scan(tf: str = "daily"):
    interval = TF_MAP.get(tf)
    if not interval:
        return {"error": "Invalid timeframe"}

    symbols = get_us_stocks()
    results = []

    for symbol in symbols:
        res = scan_symbol(symbol, interval)
        if res:
            res["timeframe"] = tf
            results.append(res)

    return {
        "timeframe": tf,
        "total": len(results),
        "results": results
    }
