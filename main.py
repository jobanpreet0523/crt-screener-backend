import os
from fastapi import FastAPI, Header, HTTPException
from batch_scan import run_nse200_scan

app = FastAPI()

CRON_SECRET = os.getenv("CRON_SECRET")

@app.get("/")
def health():
    return {"status": "CRT Screener running"}

@app.post("/cron/run")
def cron_run(x_cron_secret: str = Header(None)):
    if not CRON_SECRET:
        raise HTTPException(status_code=500, detail="CRON_SECRET not set")

    if x_cron_secret != CRON_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized cron request")

    result = run_nse200_scan()

    return {
        "status": "success",
        "scanned": result.get("count"),
        "timestamp": result.get("timestamp")
    }
