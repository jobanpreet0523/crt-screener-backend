from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# TEMP sample universe (replace with NSE 200 later)
UNIVERSE = [
    {"symbol": "RELIANCE", "close": 2500, "volume": 1200000},
    {"symbol": "TCS", "close": 3600, "volume": 300000},
    {"symbol": "INFY", "close": 1450, "volume": 900000},
]

class ScanRequest(BaseModel):
    min_price: float
    min_volume: int
    model: str

@app.post("/scan")
def scan(req: ScanRequest):
    results = []

    for stock in UNIVERSE:
        if stock["close"] >= req.min_price and stock["volume"] >= req.min_volume:
            stock["grade"] = "A+" if stock["volume"] > 1_000_000 else "B"
            results.append(stock)

    return results
