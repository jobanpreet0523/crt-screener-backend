from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="CRT Screener Backend")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root (browser safe)
@app.get("/")
def root():
    return {"status": "CRT Screener Backend Running"}

# Health check
@app.get("/health")
def health():
    return {"status": "alive"}

# CRT Scan API
@app.get("/api/crt-scan")
def crt_scan(market: str = "NIFTY", tf: str = "15m"):
    return {
        "status": "ok",
        "market": market,
        "timeframe": tf,
        "results": [
            {
                "symbol": market,
                "direction": "BUY",
                "crt_type": "Bullish CRT",
                "entry": 21850,
                "sl": 21780,
                "target": 22020,
                "grade": "A+",
                "liquidity": "BSL",
                "htf_bias": "Bullish"
            }
        ]
    }
