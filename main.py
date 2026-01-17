from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from scanner import scan_symbol
from universe import get_symbols

TF_MAP = {
    "daily": "1d",
    "4h": "4h",
    "1h": "1h",
    "15m": "15m"
}

app = FastAPI(title="CRT Screener Backend")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def root():
    return {
        "status": "OK",
        "service": "CRT Screener Backend"
    }

@app.get("/scan")
def scan(tf: str = Query("daily")):
    tf = tf.lower()

    if tf not in TF_MAP:
        return {
            "error": "Invalid timeframe",
            "allowed": list(TF_MAP.keys())
        }

    interval = TF_MAP[tf]
    symbols = get_symbols()
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
