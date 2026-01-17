from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Create app
app = FastAPI(title="CRT Screener Backend", version="1.0")

# CORS (VERY IMPORTANT for frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # later you can restrict to frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------
# Health Check (Render needs this)
# -------------------------------
@app.get("/")
def health():
    return {"status": "alive"}

# -------------------------------
# CRT Scan API
# -------------------------------
@app.get("/scan")
def scan_market():
    return {
        "status": "ok",
        "timeframe": "15m",
        "market": "NIFTY",
        "results": [
            {
                "symbol": "NIFTY",
                "direction": "BUY",
                "crt_type": "Bullish CRT",
                "entry": 21850,
                "sl": 21780,
                "target": 22020,
                "grade": "A+",
                "liquidity": "BSL",
                "htf_bias": "Bullish"
            },
            {
                "symbol": "BANKNIFTY",
                "direction": "SELL",
                "crt_type": "Bearish CRT",
                "entry": 46250,
                "sl": 46400,
                "target": 45850,
                "grade": "A",
                "liquidity": "SSL",
                "htf_bias": "Bearish"
            }
        ]
    }

