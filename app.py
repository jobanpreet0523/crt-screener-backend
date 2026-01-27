from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

# =============================
# APP INIT
# =============================
app = FastAPI(
    title="CRT Screener Backend",
    description="Backend API for CRT-based market screener",
    version="1.0.0"
)

# =============================
# CORS (VERY IMPORTANT)
# =============================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # allow Vercel / frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# =============================
# MODELS
# =============================
class ScanRequest(BaseModel):
    market: str
    timeframe: str


class ScanResult(BaseModel):
    symbol: str
    timeframe: str
    pattern: str
    bias: str


# =============================
# HEALTH CHECK
# =============================
@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "CRT Screener Backend is running"
    }


# =============================
# SCAN ENDPOINT
# =============================
@app.post("/scan", response_model=List[ScanResult])
def scan_market(request: ScanRequest):
    try:
        # 🔧 TEMP MOCK DATA (replace with real CRT logic)
        results = [
            {
                "symbol": "NASDAQ:AAPL",
                "timeframe": request.timeframe,
                "pattern": "Doji",
                "bias": "Bullish"
            },
            {
                "symbol": "NASDAQ:MSFT",
                "timeframe": request.timeframe,
                "pattern": "Liquidity Sweep",
                "bias": "Bearish"
            }
        ]

        return results

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =============================
# OPTIONAL: RENDER SAFE START
# =============================
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
