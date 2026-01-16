from fastapi import FastAPI, Query
from .scanner import run_crt_scan

app = FastAPI(
    title="CRT Screener Backend",
    description="Backend API for CRT Market Scanner",
    version="1.0.0"
)


@app.get("/")
def health_check():
    """
    Health check endpoint
    """
    return {"status": "CRT Backend Running"}


@app.get("/scan")
def scan(
    tf: str = Query(
        default="daily",
        description="Timeframe for CRT scan (daily, weekly, monthly)"
    )
):
    """
    Run CRT scan for the given timeframe
    """
    return run_crt_scan(tf)
