from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf
import pandas as pd

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message":"Stock Research API Running"}

# -------- DOJI SCREENER --------

@app.get("/screener/doji/{timeframe}")
def doji_screener(timeframe:str):

    tickers = ["AAPL","MSFT","TSLA","NVDA","AMZN"]

    results = []

    for t in tickers:

        if timeframe=="1d":
            interval="1d"
            period="5d"

        elif timeframe=="1w":
            interval="1wk"
            period="1y"

        elif timeframe=="1m":
            interval="1mo"
            period="2y"

        elif timeframe=="3m":
            interval="3mo"
            period="5y"

        else:
            return {"error":"invalid timeframe"}

        df = yf.download(t,period=period,interval=interval)

        if len(df)==0:
            continue

        last = df.iloc[-1]

        body = abs(last["Open"]-last["Close"])
        range_ = last["High"]-last["Low"]

        if body <= range_*0.1:

            results.append({
                "ticker":t,
                "open":float(last["Open"]),
                "close":float(last["Close"]),
                "high":float(last["High"]),
                "low":float(last["Low"])
            })

    return {"doji_stocks":results}

# -------- STOCK OVERVIEW --------

@app.get("/stock/{ticker}")
def stock_overview(ticker:str):

    s = yf.Ticker(ticker)

    info = s.info

    return {
        "ticker":ticker,
        "name":info.get("longName"),
        "sector":info.get("sector"),
        "industry":info.get("industry"),
        "marketCap":info.get("marketCap"),
        "price":info.get("currentPrice"),
        "pe":info.get("trailingPE"),
        "dividendYield":info.get("dividendYield")
    }

# -------- FINANCIAL STATEMENTS --------

@app.get("/financials/{ticker}")
def financials(ticker:str):

    s = yf.Ticker(ticker)

    return {
        "income":s.financials.to_dict(),
        "balance":s.balance_sheet.to_dict(),
        "cashflow":s.cashflow.to_dict()
    }

# -------- EARNINGS --------

@app.get("/earnings/{ticker}")
def earnings(ticker:str):

    s=yf.Ticker(ticker)

    return s.earnings.to_dict()

# -------- DIVIDENDS --------

@app.get("/dividends/{ticker}")
def dividends(ticker:str):

    s=yf.Ticker(ticker)

    return s.dividends.to_dict()
