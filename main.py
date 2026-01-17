from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# ✅ ADD THIS HERE (ROOT HEALTH CHECK)
@app.get("/")
def health():
    return {"status": "alive"}

# (Optional but recommended)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Your existing scan routes below
@app.get("/scan")
def scan(symbol: str, timeframe: str):
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "crt": "sample"
    }
