from fastapi import FastAPI
from engine import run_backtest
from batch_scan import scan_nse_200
from scheduler import start_scheduler

app = FastAPI(title="CRT Screener Backend")

@app.on_event("startup")
def startup_event():
    start_scheduler()

@app.get("/")
def root():
    return {"status": "CRT Backend Live 🚀"}

@app.post("/backtest")
def backtest(payload: dict):
    return run_backtest(payload)

@app.post("/scan")
def manual_scan():
    return scan_nse_200()
