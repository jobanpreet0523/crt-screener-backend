from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

# OPTIONAL imports (safe even if unused for now)
try:
    from scanner import scan_symbol
    from universe import get_us_stocks
except Exception:
    scan_symbol = None
    get_us_stocks = None

app = FastAPI(title="CRT Screener API")

# ------------------------
# CORS (IMPORTANT)
# ------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ------------------------
# HEALTH CHECK
# ------------------------
@app.get("/")
def health():
    return {
        "status": "OK",
        "service": "CRT Screener Backend"
    }

# ------------------------
# SCAN ENDPOINT (WORKING)
# ------------------------
@app.get("/scan")
def scan(tf: str = Query("daily")):
    """
    Returns CRT scan results.
    Currently returns safe mock data.
    Replace later with real CRT logic.
    """

    results = [
        {
            "symbol": "EURUSD",
            "crt": "Bullish",
            "timeframe": tf
        },
        {
            "symbol": "USDJPY",
            "crt": "Bearish",
            "timeframe": tf
        }
    ]

    return {
        "timeframe": tf,
        "total": len(results),
        "results": results
    }
