from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from data_feed import get_ohlc
from crt_structure import analyze_crt
from liquidity import analyze_liquidity

app = FastAPI(
    title="CRT Screener Backend",
    version="1.0.0"
)

# CORS (Frontend safe)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "CRT backend running 🚀"}

@app.get("/scan")
def scan_market(
    symbol: str = Query(..., description="Stock symbol", example="AAPL"),
    timeframe: str = Query(..., description="Timeframe", example="1D"),
):
    # Fetch OHLC data
    ohlc_data = get_ohlc(symbol, timeframe)

    # Validate data
    if ohlc_data is None or ohlc_data.empty:
        return {
            "error": "No OHLC data found",
            "symbol": symbol,
            "timeframe": timeframe
        }

    # Analysis
    crt_result = analyze_crt(ohlc_data)
    liquidity_result = analyze_liquidity(ohlc_data)

    # Response
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "crt": crt_result,
        "liquidity": liquidity_result,
        "data": ohlc_data.to_dict(orient="records")
    }
