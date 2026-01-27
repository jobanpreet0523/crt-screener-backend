from fastapi import FastAPI, Query, HTTPException
from data_feed import get_ohlc
from crt_structure import analyze_crt
from liquidity import analyze_liquidity

app = FastAPI(title="CRT Screener API")


@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "CRT Screener Backend is running"
    }


@app.get("/scan")
def scan_market(
    symbol: str = Query(..., example="AAPL"),
    timeframe: str = Query(..., example="1D"),
):
    df = get_ohlc(symbol, timeframe)

    if df is None:
        raise HTTPException(status_code=404, detail="No market data found")

    crt_result = analyze_crt(df)
    liquidity_result = analyze_liquidity(df)

    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "crt": crt_result,
        "liquidity": liquidity_result
    }
