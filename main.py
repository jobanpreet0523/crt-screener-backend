from fastapi import FastAPI
from data import get_ohlc
from backtest_engine import backtest_long

app = FastAPI()

@app.get("/")
def root():
    return {"status": "CRT Screener Live"}

@app.get("/backtest/{symbol}")
def backtest(symbol: str):
    df = get_ohlc(symbol.upper(), "2022-01-01", "2025-01-01")
    if df.empty:
        return {"error": "No data"}

    trades = backtest_long(df)
    return {
        "symbol": symbol,
        "total_trades": len(trades),
        "wins": int((trades["result"] == "WIN").sum()),
        "losses": int((trades["result"] == "LOSS").sum())
    }
