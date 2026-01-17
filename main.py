from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health():
    return {"status": "alive"}

@app.get("/api/crt-scan")
def crt_scan(market: str = "NIFTY", tf: str = "15m"):
    return {
        "status": "ok",
        "timeframe": tf,
        "market": market,
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
            }
        ]
    }
