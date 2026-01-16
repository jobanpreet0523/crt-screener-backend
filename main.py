from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from scanner import scan_symbol

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

TF_MAP = {
    "daily": "1d",
    "4h": "1h",
    "1h": "1h",
    "15m": "15m"
}

FOREX_PAIRS = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X",
    "AUDUSD=X",
    "USDCHF=X",
    "USDCAD=X",
    "NZDUSD=X"
]

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

    results = []

    for symbol in FOREX_PAIRS:
        res = scan_symbol(symbol, interval)
        if res:
            results.append({
                "symbol": symbol.replace("=X", ""),
                "crt": res,
                "timeframe": tf
            })

    return {
        "timeframe": tf,
        "total": len(results),
        "results": results
    }
