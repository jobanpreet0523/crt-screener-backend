from fastapi import FastAPI, Query
from datetime import datetime

from crt_scanner import scan_crt_setup

app = FastAPI(title="CRT Screener Backend")


@app.get("/")
def health():
    return {"status": "CRT backend running"}


@app.get("/scan/crt")
def scan_crt(
    symbol: str = Query(..., example="NAS100"),
):
    """
    CRT Scan API
    """

    # ⚠️ MOCK DATA for now (real feed comes later)
    htf_candles = [
        {"open": 100, "high": 110, "low": 95, "close": 108},
        {"open": 108, "high": 115, "low": 105, "close": 112},
    ]

    ltf_candles = [
        {"open": 112, "high": 113, "low": 109, "close": 110},
        {"open": 110, "high": 111, "low": 106, "close": 107},
    ]

    result = scan_crt_setup(
        symbol=symbol,
        htf_candles=htf_candles,
        ltf_candles=ltf_candles,
        timestamp_utc=datetime.utcnow()
    )

    return result
