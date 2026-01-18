from fastapi import FastAPI
from batch_scan import run_batch_scan

app = FastAPI(title="CRT Screener Backend")

@app.get("/")
def root():
    return {"status": "alive"}

@app.get("/api/crt-scan")
def crt_scan():
    return {
        "status": "ok",
        "market": "NIFTY",
        "timeframe": "15m",
        "results": run_batch_scan()
    }
