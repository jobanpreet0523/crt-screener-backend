# app.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse

from datetime import datetime

from data_feed import RestDataFeed
from multi_scanner import scan_markets

app = FastAPI(title="CRT Scanner API")

# TEMP feed (CSV / REST mock)
feed = RestDataFeed("data/sample.csv")

# Market universe
SYMBOLS = {
    "EURUSD": {"htf": "1h", "ltf": "5m"},
    "GBPUSD": {"htf": "1h", "ltf": "5m"},
    "NQ":     {"htf": "4h", "ltf": "5m"},
    "ES":     {"htf": "4h", "ltf": "5m"},
}


@app.get("/scan/all")
def scan_all():
    results = scan_markets(
        feed=feed,
        symbols=SYMBOLS,
        timestamp=datetime.utcnow()
    )
    return JSONResponse(results)


@app.get("/scan/a_plus")
def scan_a_plus():
    results = scan_markets(
        feed=feed,
        symbols=SYMBOLS,
        timestamp=datetime.utcnow()
    )

    a_plus = [r for r in results if r["grade"] == "A_PLUS"]
    return JSONResponse(a_plus)
