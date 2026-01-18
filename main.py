from fastapi import FastAPI
from batch_scan import run_batch_scan
from engine import run_single_scan

app = FastAPI()

@app.get("/")
def health():
    return {"status": "ok"}

# 🔥 SINGLE CRT SCAN (used by frontend)
@app.get("/api/crt-scan")
def crt_scan(symbol: str = "NIFTY", tf: str = "15m"):
    return run_single_scan(symbol, tf)

# 🔥 NSE BATCH SCAN (200 stocks)
@app.get("/api/batch-scan")
def batch_scan():
    return run_batch_scan()
