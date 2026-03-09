from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import yfinance as yf

app = FastAPI()

# allow frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def home():
    return {"message": "Stock Research Backend Running"}

# -------------------------
# DOJI SCREENER
# -------------------------

@app.get("/screener/doji/{tf}")
def doji_screener(tf: str):

    tickers = ["AAPL","MSFT","TSLA","NVDA","AMZN"]

    results = []

    for ticker in tickers:

        if tf == "1d":
            interval="1d"
            period="5d"

        elif tf == "1w":
            interval="1wk"
            period="1y"

        elif tf == "1m":
            interval="1mo"
            period="2y"

        elif tf == "3m":
            interval="3mo"
            period="5y"

        else:
            return {"error":"invalid timeframe"}

        df = yf.download(ticker, period=period, interval=interval)

        if len(df) == 0:
            continue

        last = df.iloc[-1]

        body = abs(last["Open"] - last["Close"])
        rng = last["High"] - last["Low"]

        if body <= rng * 0.1:
            results.append(ticker)

    return {"doji_stocks": results}


# -------------------------
# STOCK OVERVIEW
# -------------------------

@app.get("/stock/{ticker}")
def stock_overview(ticker: str):

    stock = yf.Ticker(ticker)
    info = stock.info

    return {
        "ticker": ticker.upper(),
        "name": info.get("longName"),
        "price": info.get("currentPrice"),
        "marketCap": info.get("marketCap"),
        "sector": info.get("sector"),
        "industry": info.get("industry"),
        "pe": info.get("trailingPE"),
        "dividendYield": info.get("dividendYield")
    }


# -------------------------
# FINANCIAL STATEMENTS
# -------------------------

@app.get("/financials/{ticker}")
def financials(ticker: str):

    stock = yf.Ticker(ticker)

    return {
        "income_statement": stock.financials.to_dict(),
        "balance_sheet": stock.balance_sheet.to_dict(),
        "cashflow": stock.cashflow.to_dict()
    }


# -------------------------
# AI RESEARCH PLACEHOLDER
# -------------------------

@app.get("/ai/{ticker}")
def ai_research(ticker: str):

    return {
        "analysis": f"""
        AI analysis for {ticker}

        Business Model:
        Company generates revenue through its main products and services.

        Growth:
        Revenue and earnings growth should be analyzed from financial statements.

        Risks:
        Market competition, economic conditions, and debt levels.

        Investors should review financials before making decisions.
        """
    }
