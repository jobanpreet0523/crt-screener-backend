from fastapi import FastAPI
from scanner import scan_symbol

app = FastAPI(title="CRT Screener Backend")


@app.get("/")
def root():
    return {"status": "CRT backend running"}


@app.get("/scan")
def scan(symbol: str = "EURUSD=X"):
    return scan_symbol(symbol)
