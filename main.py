from fastapi import FastAPI

app = FastAPI()

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
