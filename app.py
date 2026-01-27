from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(
    title="CRT Screener API",
    version="1.0.0"
)

# CORS (VERY IMPORTANT)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # later restrict to Vercel URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------- MODELS --------
class ScanRequest(BaseModel):
    market: str
    timeframe: str


# -------- ROUTES --------
@app.get("/")
def health_check():
    return {"status": "CRT Screener backend running"}

@app.post("/scan")
def scan_market(req: ScanRequest):
    # Dummy response (replace with real logic)
    return {
        "market": req.market,
        "timeframe": req.timeframe,
        "results": [
            {
                "symbol": "AAPL",
                "pattern": "CRT Doji",
                "bias": "Bullish",
                "price": 195.40
            },
            {
                "symbol": "MSFT",
                "pattern": "CRT Liquidity Sweep",
                "bias": "Bearish",
                "price": 412.10
            }
        ]
    }
