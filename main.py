from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# import your local files (same folder)
from scanner import run_scan

app = FastAPI(title="CRT Screener Backend")

# --------------------
# ✅ CORS (FIXED)
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all frontends
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Health Check (IMPORTANT for Render)
# --------------------
@app.get("/")
def root():
    return {"status": "CRT Screener Backend is running"}

# --------------------
# Main Scan API
# --------------------
@app.get("/scan")
def scan(tf: str = "daily"):
    """
    Example:
    /scan?tf=daily
    /scan?tf=4h
    """
    data = run_scan(timeframe=tf)
    return data
