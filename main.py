from fastapi import FastAPI
from batch_scan import run_batch_scan

app = FastAPI()

# 🔹 Health check (Render needs this)
@app.get("/")
def health():
    return {"status": "alive"}

# 🔹 CRT Screener API (THIS IS STEP 6)
@app.get("/scan")
def scan(
    market: str = "NIFTY",
    timeframe: str = "15m"
):
    results = run_batch_scan(market, timeframe)
    return {
        "status": "ok",
        "market": market,
        "timeframe": timeframe,
        "results": results
    }
