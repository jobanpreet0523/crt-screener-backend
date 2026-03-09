from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home route (fix 404)
@app.get("/")
def home():
    return {"message": "CRT Screener Backend Running"}

# Simple Screener (Doji Example)
@app.get("/scan")
def scan():
    ticker = "AAPL"
    data = yf.download(ticker, period="5d", interval="1d")

    if len(data) == 0:
        return {"error": "No data"}

    last = data.iloc[-1]

    open_price = float(last["Open"])
    close_price = float(last["Close"])
    high = float(last["High"])
    low = float(last["Low"])

    body = abs(open_price - close_price)
    candle_range = high - low

    doji = body <= candle_range * 0.1

    return {
        "ticker": ticker,
        "open": open_price,
        "close": close_price,
        "high": high,
        "low": low,
        "doji": doji
    }

# Stock Information
@app.get("/stock/{ticker}")
def get_stock(ticker: str):
    stock = yf.Ticker(ticker)

    info = stock.info

    return {
        "ticker": ticker.upper(),
        "name": info.get("longName"),
        "price": info.get("currentPrice"),
        "market_cap": info.get("marketCap"),
        "pe_ratio": info.get("trailingPE"),
        "sector": info.get("sector"),
        "industry": info.get("industry")
    }

# Financial Statements
@app.get("/financials/{ticker}")
def financials(ticker: str):
    stock = yf.Ticker(ticker)

    income = stock.financials
    balance = stock.balance_sheet
    cashflow = stock.cashflow

    return {
        "income_statement": income.to_dict(),
        "balance_sheet": balance.to_dict(),
        "cash_flow": cashflow.to_dict()
    }
