# main.py

from fastapi import FastAPI
from batch_scan import run_batch_scan

app = FastAPI()

@app.get("/")
def health():
    return {"status": "CRT backend running"}

@app.post("/scan")
def scan(data: dict):
    symbols = data.get("symbols", [])
    timeframe = data.get("timeframe", "15m")
    return run_batch_scan(symbols, timeframe)
