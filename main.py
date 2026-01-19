from fastapi import FastAPI, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os

# -------------------------------------------------
# App Init
# -------------------------------------------------
app = FastAPI(title="CRT Screener Backend")

# -------------------------------------------------
# CORS (React Frontend)
# -------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Secrets
# -------------------------------------------------
CRON_SECRET = os.getenv("CRON_SECRET", "dev-secret")

# -------------------------------------------------
# Health Check
# -------------------------------------------------
@app.get("/")
def health():
    return {"status": "ok"}

# -------------------------------------------------
# Backtest Endpoint (React → Backend)
# -------------------------------------------------
@app.post("/backtest")
def run_backtest(payload: dict):
    """
    React frontend sends strategy params here
    """
    return {
        "message": "Backtest endpoint working",
        "input": payload
    }

# -------------------------------------------------
# Secure Cron Endpoint (GitHub Actions)
# -------------------------------------------------
@app.post("/cron/run")
def cron_run(x_cron_secret: str = Header(None)):
    if x_cron_secret != CRON_SECRET:
        raise HTTPException(status_code=401, detail="Unauthorized")

    from cron_scan import run_nse_scan
    run_nse_scan()

    return {"status": "NSE scan completed successfully"}
