# ============================================================
#  CRT Screener Backend — Upgraded main.py
#  Run:  uvicorn main:app --reload --port 8000
# ============================================================

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timezone, timedelta
from typing import Optional

app = FastAPI(
    title="CRT Screener API",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─────────────────────────────────────────────────────────────
#  NSE 200 UNIVERSE  (add .NS suffix for Yahoo Finance)
# ─────────────────────────────────────────────────────────────
NSE_SYMBOLS = [
    "RELIANCE","TCS","HDFCBANK","INFY","ICICIBANK","HINDUNILVR","SBIN",
    "BHARTIARTL","BAJFINANCE","KOTAKBANK","LT","AXISBANK","WIPRO","MARUTI",
    "SUNPHARMA","HCLTECH","TITAN","NTPC","ONGC","DRREDDY","TATASTEEL",
    "COALINDIA","TATAMOTORS","JSWSTEEL","CIPLA","INDUSINDBK","DIVISLAB",
    "BPCL","HEROMOTOCO","APOLLOHOSP","TATACONSUM","ZOMATO","HAVELLS",
    "VEDL","BALKRISIND","MUTHOOTFIN","PIDILIND","POWERGRID","NESTLEIND",
    "EICHERMOT","BAJAJFINSV","GRASIM","ULTRACEMCO","TECHM","ASIANPAINT",
    "ITC","M&M","ADANIPORTS","SBILIFE","ADANIENT","DABUR","MARICO",
    "COLPAL","TATAPOWER","TORNTPHARM","LUPIN","BIOCON","AUROPHARMA",
    "IPCALAB","ALKEM","MRF","BOSCHLTD","CUMMINSIND","ABB","SIEMENS",
    "BHEL","BEL","PAGEIND","BERGEPAINT","KANSAINER","NAUKRI",
]

# US stocks kept for backward compatibility
US_SYMBOLS = ["AAPL","MSFT","TSLA","NVDA","AMZN","GOOGL","META","NFLX"]

SECTOR_MAP = {
    "RELIANCE":"Energy","TCS":"IT","HDFCBANK":"Bank","INFY":"IT",
    "ICICIBANK":"Bank","HINDUNILVR":"FMCG","SBIN":"Bank","BHARTIARTL":"Telecom",
    "BAJFINANCE":"Bank","KOTAKBANK":"Bank","LT":"Capital Goods","AXISBANK":"Bank",
    "WIPRO":"IT","MARUTI":"Auto","SUNPHARMA":"Pharma","HCLTECH":"IT",
    "TITAN":"FMCG","NTPC":"Power","ONGC":"Energy","DRREDDY":"Pharma",
    "TATASTEEL":"Metal","COALINDIA":"Energy","TATAMOTORS":"Auto","JSWSTEEL":"Metal",
    "CIPLA":"Pharma","INDUSINDBK":"Bank","DIVISLAB":"Pharma","BPCL":"Energy",
    "HEROMOTOCO":"Auto","APOLLOHOSP":"Healthcare","TATACONSUM":"FMCG",
    "ZOMATO":"Internet","HAVELLS":"Capital Goods","VEDL":"Metal",
    "BALKRISIND":"Auto","MUTHOOTFIN":"Bank","PIDILIND":"Chemicals",
    "POWERGRID":"Power","NESTLEIND":"FMCG","EICHERMOT":"Auto","BAJAJFINSV":"Bank",
    "GRASIM":"Cement","ULTRACEMCO":"Cement","TECHM":"IT","ASIANPAINT":"FMCG",
    "ITC":"FMCG","M&M":"Auto","ADANIPORTS":"Infra","SBILIFE":"Insurance",
}

# ─────────────────────────────────────────────────────────────
#  HELPERS
# ─────────────────────────────────────────────────────────────

def nse(sym: str) -> str:
    """Add .NS suffix for NSE symbols."""
    return f"{sym}.NS"

def tf_params(tf: str):
    """Map timeframe string → yfinance (period, interval)."""
    mapping = {
        "1d":  ("5d",  "1d"),
        "1w":  ("1y",  "1wk"),
        "1m":  ("2y",  "1mo"),
        "3m":  ("5y",  "3mo"),
        "1h":  ("5d",  "1h"),
        "15m": ("1d",  "15m"),
    }
    return mapping.get(tf, ("5d", "1d"))

def calc_rsi(closes: pd.Series, period: int = 14) -> float:
    """Compute RSI from a price series."""
    delta = closes.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(period).mean().iloc[-1]
    avg_loss = loss.rolling(period).mean().iloc[-1]
    if avg_loss == 0:
        return 100.0
    rs = avg_gain / avg_loss
    return round(float(100 - (100 / (1 + rs))), 1)

def calc_ema(closes: pd.Series, period: int) -> float:
    return float(closes.ewm(span=period, adjust=False).mean().iloc[-1])

def calc_macd(closes: pd.Series):
    ema12 = closes.ewm(span=12, adjust=False).mean()
    ema26 = closes.ewm(span=26, adjust=False).mean()
    macd_line = ema12 - ema26
    signal = macd_line.ewm(span=9, adjust=False).mean()
    return round(float(macd_line.iloc[-1]), 3), round(float(signal.iloc[-1]), 3)

def market_status():
    """Check if NSE market is open right now."""
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist)
    if now.weekday() >= 5:
        return False, now.strftime("%H:%M IST")
    open_t  = now.replace(hour=9,  minute=15, second=0, microsecond=0)
    close_t = now.replace(hour=15, minute=30, second=0, microsecond=0)
    is_open = open_t <= now <= close_t
    return is_open, now.strftime("%H:%M IST")

# ─────────────────────────────────────────────────────────────
#  CRT PATTERN DETECTION
# ─────────────────────────────────────────────────────────────

def detect_crt_pattern(df: pd.DataFrame) -> dict:
    """
    CRT = Candle Range Theory
    Looks for: HTF range → LTF sweep → structure confirmation
    Returns bias (bullish/bearish/none) and grade (A_PLUS/VALID/WEAK/NO_TRADE)
    """
    if len(df) < 5:
        return {"bias": None, "grade": "NO_TRADE", "crt": False}

    # Use last 5 candles
    candles = df.tail(5)
    last    = candles.iloc[-1]
    prev    = candles.iloc[-2]
    prev2   = candles.iloc[-3]

    opens  = candles["Open"].values
    highs  = candles["High"].values
    lows   = candles["Low"].values
    closes = candles["Close"].values

    # ── Doji detection (small body vs range)
    body  = abs(float(last["Close"]) - float(last["Open"]))
    rng   = float(last["High"]) - float(last["Low"])
    is_doji = rng > 0 and (body / rng) < 0.1

    # ── Swing High / Swing Low sweep
    swing_high = max(highs[:-1])
    swing_low  = min(lows[:-1])
    swept_bsl  = float(last["High"]) > swing_high and float(last["Close"]) < swing_high
    swept_ssl  = float(last["Low"])  < swing_low  and float(last["Close"]) > swing_low

    # ── Structure shift
    bullish_shift = (float(prev["Close"]) < float(prev["Open"])) and (float(last["Close"]) > float(prev["High"]))
    bearish_shift = (float(prev["Close"]) > float(prev["Open"])) and (float(last["Close"]) < float(prev["Low"]))

    # ── Session check
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist)
    h, m = now.hour, now.minute
    in_london  = (13 <= h < 17)          # 13:30–17:00 IST ≈ London
    in_newyork = (18 <= h < 23)          # 18:30–23:00 IST ≈ New York
    in_asia    = (4  <= h < 9)           # 4:00–9:15 IST  ≈ Asia/pre-market

    bias, grade = None, "NO_TRADE"
    crt_detected = False

    if swept_ssl and bullish_shift:
        bias = "bullish"
        crt_detected = True
        grade = "WEAK"
        if in_london or in_newyork:
            grade = "VALID"
        if (in_london or in_newyork) and is_doji:
            grade = "A_PLUS"
    elif swept_bsl and bearish_shift:
        bias = "bearish"
        crt_detected = True
        grade = "WEAK"
        if in_london or in_newyork:
            grade = "VALID"
        if (in_london or in_newyork) and is_doji:
            grade = "A_PLUS"

    return {
        "bias":    bias,
        "grade":   grade,
        "crt":     crt_detected,
        "swept_bsl": swept_bsl,
        "swept_ssl": swept_ssl,
        "is_doji": is_doji,
    }

# ─────────────────────────────────────────────────────────────
#  CORE SCREENER FUNCTION
# ─────────────────────────────────────────────────────────────

def screen_stock(sym: str, market: str, tf: str) -> Optional[dict]:
    """Fetch data + run all pattern checks for one symbol."""
    try:
        ticker_sym = nse(sym) if market == "NSE" else sym
        period, interval = tf_params(tf)
        df = yf.download(ticker_sym, period=period, interval=interval, progress=False, auto_adjust=True)

        if df is None or len(df) < 3:
            return None

        # Flatten multi-level columns if present
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        last = df.iloc[-1]
        prev = df.iloc[-2]

        price   = round(float(last["Close"]), 2)
        open_   = round(float(last["Open"]),  2)
        high    = round(float(last["High"]),   2)
        low     = round(float(last["Low"]),    2)
        vol     = int(last["Volume"]) if not pd.isna(last["Volume"]) else 0
        prev_c  = round(float(prev["Close"]),  2)
        chg     = round(((price - prev_c) / prev_c) * 100, 2) if prev_c else 0

        rsi     = calc_rsi(df["Close"]) if len(df) >= 15 else 50.0
        macd_v, macd_sig = calc_macd(df["Close"]) if len(df) >= 26 else (0, 0)

        # 52-week data
        df_1y  = yf.download(ticker_sym, period="1y", interval="1d", progress=False, auto_adjust=True)
        if isinstance(df_1y.columns, pd.MultiIndex):
            df_1y.columns = df_1y.columns.get_level_values(0)
        wk52h  = round(float(df_1y["High"].max()), 2)  if len(df_1y) > 0 else high
        wk52l  = round(float(df_1y["Low"].min()),  2)  if len(df_1y) > 0 else low
        vol_avg = int(df_1y["Volume"].mean())           if len(df_1y) > 0 else vol

        # CRT pattern
        crt = detect_crt_pattern(df)

        # Pattern flags
        body     = abs(price - open_)
        rng      = high - low
        is_doji  = rng > 0 and (body / rng) < 0.1
        is_hammer = (rng > 0
                     and (price - low) / rng > 0.65
                     and body / rng < 0.3)
        is_shooting_star = (rng > 0
                            and (high - price) / rng > 0.65
                            and body / rng < 0.3)

        return {
            "symbol":    sym,
            "market":    market,
            "price":     price,
            "open":      open_,
            "high":      high,
            "low":       low,
            "change":    chg,
            "volume":    vol,
            "vol_avg":   vol_avg,
            "rsi":       rsi,
            "macd":      macd_v,
            "macd_sig":  macd_sig,
            "wk52h":     wk52h,
            "wk52l":     wk52l,
            "sector":    SECTOR_MAP.get(sym, "Other"),
            # Pattern flags
            "is_doji":           is_doji,
            "is_hammer":         is_hammer,
            "is_shooting_star":  is_shooting_star,
            "is_volume_surge":   vol > vol_avg * 2 if vol_avg else False,
            "is_rsi_oversold":   rsi < 30,
            "is_rsi_overbought": rsi > 70,
            "is_macd_bullish":   macd_v > macd_sig,
            "is_near_52h":       wk52h > 0 and price / wk52h > 0.95,
            # CRT data
            "crt_bias":          crt["bias"],
            "crt_grade":         crt["grade"],
            "crt_detected":      crt["crt"],
        }
    except Exception as e:
        print(f"[screen_stock] {sym}: {e}")
        return None

# ─────────────────────────────────────────────────────────────
#  ROUTES
# ─────────────────────────────────────────────────────────────

@app.get("/")
def root():
    is_open, time_str = market_status()
    return {
        "status":      "LIVE",
        "version":     "2.0.0",
        "market_open": is_open,
        "ist_time":    time_str,
        "message":     "CRT Screener Backend Running",
    }

@app.get("/health")
def health():
    return {"ok": True}


# ── DOJI SCREENER (backward compatible + upgraded) ────────────
@app.get("/screener/doji/{tf}")
def doji_screener(
    tf:     str,
    market: str = Query("NSE", description="NSE or US"),
    sector: str = Query("all"),
    limit:  int = Query(50),
):
    symbols = NSE_SYMBOLS if market == "NSE" else US_SYMBOLS
    results = []
    for sym in symbols[:limit]:
        d = screen_stock(sym, market, tf)
        if d and d["is_doji"]:
            if sector != "all" and d["sector"] != sector:
                continue
            results.append(d)
    return {"scan": "doji", "tf": tf, "count": len(results), "results": results}


# ── UNIVERSAL SCAN ENDPOINT ────────────────────────────────────
SCAN_FILTERS = {
    "doji":           lambda d: d["is_doji"],
    "hammer":         lambda d: d["is_hammer"],
    "shooting_star":  lambda d: d["is_shooting_star"],
    "rsi_oversold":   lambda d: d["is_rsi_oversold"],
    "rsi_overbought": lambda d: d["is_rsi_overbought"],
    "volume_surge":   lambda d: d["is_volume_surge"],
    "macd_bullish":   lambda d: d["is_macd_bullish"],
    "near_52h":       lambda d: d["is_near_52h"],
    "crt_aplus":      lambda d: d["crt_grade"] == "A_PLUS",
    "crt_valid":      lambda d: d["crt_grade"] in ("A_PLUS", "VALID"),
    "crt_bullish":    lambda d: d["crt_detected"] and d["crt_bias"] == "bullish",
    "crt_bearish":    lambda d: d["crt_detected"] and d["crt_bias"] == "bearish",
    "all":            lambda d: True,
}

@app.get("/scan")
def universal_scan(
    type:       str   = Query("doji"),
    tf:         str   = Query("1d"),
    market:     str   = Query("NSE"),
    sector:     str   = Query("all"),
    min_price:  float = Query(0),
    max_price:  float = Query(9_999_999),
    min_rsi:    float = Query(0),
    max_rsi:    float = Query(100),
    min_vol:    float = Query(0),   # in Lakhs
    limit:      int   = Query(50),
):
    symbols = NSE_SYMBOLS if market == "NSE" else US_SYMBOLS
    scan_fn = SCAN_FILTERS.get(type, SCAN_FILTERS["all"])
    results = []

    for sym in symbols[:limit]:
        d = screen_stock(sym, market, tf)
        if d is None:
            continue
        if not scan_fn(d):
            continue
        if sector != "all" and d["sector"] != sector:
            continue
        if not (min_price <= d["price"] <= max_price):
            continue
        if not (min_rsi <= d["rsi"] <= max_rsi):
            continue
        if d["volume"] / 100_000 < min_vol:
            continue
        results.append(d)

    results.sort(key=lambda x: abs(x["change"]), reverse=True)
    return {
        "ok":      True,
        "scan":    type,
        "tf":      tf,
        "market":  market,
        "count":   len(results),
        "results": results,
    }


# ── STOCK OVERVIEW (upgraded) ─────────────────────────────────
@app.get("/stock/{ticker}")
def stock_overview(ticker: str, market: str = Query("NSE")):
    try:
        sym = nse(ticker) if market == "NSE" else ticker
        stock = yf.Ticker(sym)
        info  = stock.info

        # Historical for chart data (30 days)
        hist = stock.history(period="1mo")
        chart = []
        if not hist.empty:
            for dt, row in hist.iterrows():
                chart.append({
                    "date":  str(dt)[:10],
                    "open":  round(float(row["Open"]),  2),
                    "high":  round(float(row["High"]),  2),
                    "low":   round(float(row["Low"]),   2),
                    "close": round(float(row["Close"]), 2),
                    "vol":   int(row["Volume"]),
                })

        return {
            "ticker":        ticker.upper(),
            "name":          info.get("longName") or info.get("shortName"),
            "price":         info.get("currentPrice") or info.get("regularMarketPrice"),
            "change":        info.get("regularMarketChangePercent"),
            "marketCap":     info.get("marketCap"),
            "sector":        info.get("sector") or SECTOR_MAP.get(ticker, "Other"),
            "industry":      info.get("industry"),
            "pe":            info.get("trailingPE"),
            "forwardPE":     info.get("forwardPE"),
            "dividendYield": info.get("dividendYield"),
            "52wHigh":       info.get("fiftyTwoWeekHigh"),
            "52wLow":        info.get("fiftyTwoWeekLow"),
            "avgVolume":     info.get("averageVolume"),
            "beta":          info.get("beta"),
            "roe":           info.get("returnOnEquity"),
            "debtToEquity":  info.get("debtToEquity"),
            "chart":         chart,
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ── FINANCIALS ────────────────────────────────────────────────
@app.get("/financials/{ticker}")
def financials(ticker: str, market: str = Query("NSE")):
    try:
        sym   = nse(ticker) if market == "NSE" else ticker
        stock = yf.Ticker(sym)
        return {
            "ticker":           ticker.upper(),
            "income_statement": stock.financials.to_dict()     if stock.financials is not None else {},
            "balance_sheet":    stock.balance_sheet.to_dict()  if stock.balance_sheet is not None else {},
            "cashflow":         stock.cashflow.to_dict()        if stock.cashflow is not None else {},
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ── INDICES ───────────────────────────────────────────────────
@app.get("/indices")
def indices():
    try:
        def get_index(sym):
            t = yf.Ticker(sym)
            h = t.history(period="2d")
            if h.empty:
                return None
            price  = round(float(h.iloc[-1]["Close"]), 2)
            prev   = round(float(h.iloc[-2]["Close"]), 2) if len(h) > 1 else price
            change = round(((price - prev) / prev) * 100, 2)
            return {"price": price, "change": change}

        return {
            "nifty50":    get_index("^NSEI"),
            "sensex":     get_index("^BSESN"),
            "banknifty":  get_index("^NSEBANK"),
            "sp500":      get_index("^GSPC"),
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ── QUOTE (batch) ─────────────────────────────────────────────
@app.get("/quote")
def batch_quote(symbols: str = Query(...), market: str = Query("NSE")):
    syms    = [s.strip().upper() for s in symbols.split(",")][:20]
    results = []
    for sym in syms:
        try:
            ticker_sym = nse(sym) if market == "NSE" else sym
            t  = yf.Ticker(ticker_sym)
            h  = t.history(period="2d")
            if h.empty:
                continue
            price  = round(float(h.iloc[-1]["Close"]), 2)
            prev   = round(float(h.iloc[-2]["Close"]), 2) if len(h) > 1 else price
            change = round(((price - prev) / prev) * 100, 2)
            results.append({"symbol": sym, "price": price, "change": change})
        except Exception:
            pass
    return {"ok": True, "quotes": results}


# ── AI RESEARCH (upgraded with real data context) ─────────────
@app.get("/ai/{ticker}")
def ai_research(ticker: str, market: str = Query("NSE")):
    try:
        sym   = nse(ticker) if market == "NSE" else ticker
        stock = yf.Ticker(sym)
        info  = stock.info
        name  = info.get("longName") or ticker
        price = info.get("currentPrice") or "N/A"
        pe    = info.get("trailingPE")
        sector = info.get("sector") or SECTOR_MAP.get(ticker, "N/A")
        roe   = info.get("returnOnEquity")
        beta  = info.get("beta")
        div   = info.get("dividendYield")
        desc  = info.get("longBusinessSummary", "No description available.")[:400]

        # Pull last 1 year for RSI
        hist = stock.history(period="1y")
        rsi  = calc_rsi(hist["Close"]) if len(hist) >= 15 else None
        macd_v, macd_sig = calc_macd(hist["Close"]) if len(hist) >= 26 else (None, None)

        signal = "NEUTRAL"
        if rsi and rsi < 30:
            signal = "OVERSOLD — Potential Buy Zone"
        elif rsi and rsi > 70:
            signal = "OVERBOUGHT — Caution / Potential Sell"
        elif macd_v and macd_v > macd_sig:
            signal = "MACD BULLISH — Momentum Positive"

        return {
            "ticker": ticker.upper(),
            "name":   name,
            "signal": signal,
            "analysis": {
                "business":   desc,
                "technicals": {
                    "rsi":        rsi,
                    "macd":       macd_v,
                    "macd_signal":macd_sig,
                    "momentum":   signal,
                },
                "fundamentals": {
                    "sector":       sector,
                    "pe_ratio":     pe,
                    "roe":          f"{round(roe*100,1)}%" if roe else "N/A",
                    "beta":         beta,
                    "dividend":     f"{round(div*100,2)}%" if div else "0%",
                },
                "price":  price,
                "risks": [
                    "Market-wide corrections can affect even strong stocks",
                    "Sector-specific regulatory changes",
                    "Global macro factors (inflation, rate hikes)",
                    "Always review latest financial statements before investing",
                ],
            }
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# ── CRT SCAN (dedicated endpoint) ────────────────────────────
@app.get("/crt/scan")
def crt_scan(
    tf:     str = Query("1d"),
    market: str = Query("NSE"),
    grade:  str = Query("all"),   # all / A_PLUS / VALID / WEAK
    limit:  int = Query(50),
):
    symbols = NSE_SYMBOLS if market == "NSE" else US_SYMBOLS
    results = []
    for sym in symbols[:limit]:
        d = screen_stock(sym, market, tf)
        if d and d["crt_detected"]:
            if grade != "all" and d["crt_grade"] != grade:
                continue
            results.append(d)
    results.sort(key=lambda x: (
        {"A_PLUS": 0, "VALID": 1, "WEAK": 2, "NO_TRADE": 3}.get(x["crt_grade"], 9)
    ))
    return {
        "ok":     True,
        "scan":   "crt",
        "tf":     tf,
        "grade":  grade,
        "count":  len(results),
        "results":results,
    }
