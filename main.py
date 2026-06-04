# ============================================================
#  CRT Screener Backend — Fast Parallel Version
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
import asyncio
from concurrent.futures import ThreadPoolExecutor
import threading

app = FastAPI(title="CRT Screener API", version="3.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── NSE 200 UNIVERSE ────────────────────────────────────────
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
    "MRF","BOSCHLTD","CUMMINSIND","ABB","SIEMENS","BHEL","BEL","NAUKRI",
]

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
    "ZOMATO":"Internet","NAUKRI":"Internet","HAVELLS":"Capital Goods",
    "VEDL":"Metal","BALKRISIND":"Auto","MUTHOOTFIN":"Bank","PIDILIND":"Chemicals",
    "POWERGRID":"Power","NESTLEIND":"FMCG","EICHERMOT":"Auto","BAJAJFINSV":"Bank",
    "GRASIM":"Cement","ULTRACEMCO":"Cement","TECHM":"IT","ASIANPAINT":"FMCG",
    "ITC":"FMCG","M&M":"Auto","ADANIPORTS":"Infra","SBILIFE":"Insurance",
}

MCAP_MAP = {
    "RELIANCE":"Large","TCS":"Large","HDFCBANK":"Large","INFY":"Large",
    "ICICIBANK":"Large","HINDUNILVR":"Large","SBIN":"Large","BHARTIARTL":"Large",
    "BAJFINANCE":"Large","KOTAKBANK":"Large","LT":"Large","AXISBANK":"Large",
    "WIPRO":"Large","MARUTI":"Large","SUNPHARMA":"Large","HCLTECH":"Large",
    "TITAN":"Large","NTPC":"Large","ONGC":"Large","DRREDDY":"Large",
    "TATASTEEL":"Large","COALINDIA":"Large","TATAMOTORS":"Large","ITC":"Large",
    "M&M":"Large","ADANIPORTS":"Large","NESTLEIND":"Large","ASIANPAINT":"Large",
    "JSWSTEEL":"Mid","CIPLA":"Mid","INDUSINDBK":"Mid","DIVISLAB":"Mid",
    "BPCL":"Mid","HEROMOTOCO":"Mid","APOLLOHOSP":"Mid","TATACONSUM":"Mid",
    "ZOMATO":"Mid","NAUKRI":"Mid","HAVELLS":"Mid","GRASIM":"Mid",
    "ULTRACEMCO":"Large","PIDILIND":"Mid",
    "VEDL":"Small","BALKRISIND":"Small","MUTHOOTFIN":"Small",
}

# ─── IN-MEMORY CACHE ─────────────────────────────────────────
cache = {}
cache_time = {}
CACHE_TTL = 900  # 15 minutes

# ─── THREAD POOL FOR PARALLEL FETCHING ───────────────────────
executor = ThreadPoolExecutor(max_workers=10)

# ─── HELPERS ─────────────────────────────────────────────────
def nse(sym): return f"{sym}.NS"

def tf_params(tf):
    return {
        "1d":  ("5d",  "1d"),
        "1w":  ("1y",  "1wk"),
        "1m":  ("2y",  "1mo"),
        "3m":  ("5y",  "3mo"),
        "1h":  ("5d",  "1h"),
        "15m": ("1d",  "15m"),
    }.get(tf, ("5d","1d"))

def calc_rsi(closes, period=14):
    if len(closes) < period+1: return 50.0
    delta = closes.diff()
    gain = delta.clip(lower=0).rolling(period).mean().iloc[-1]
    loss = (-delta.clip(upper=0)).rolling(period).mean().iloc[-1]
    if loss == 0: return 100.0
    return round(float(100 - 100/(1+gain/loss)), 1)

def calc_macd(closes):
    if len(closes) < 26: return 0.0, 0.0
    ema12 = closes.ewm(span=12,adjust=False).mean()
    ema26 = closes.ewm(span=26,adjust=False).mean()
    macd  = ema12 - ema26
    sig   = macd.ewm(span=9,adjust=False).mean()
    return round(float(macd.iloc[-1]),3), round(float(sig.iloc[-1]),3)

def doji_score(o,c,h,l):
    r = h-l
    return abs(c-o)/r if r>0 else 1

def market_status():
    ist = timezone(timedelta(hours=5,minutes=30))
    now = datetime.now(ist)
    if now.weekday() >= 5: return False, now.strftime("%H:%M IST")
    o = now.replace(hour=9,minute=15,second=0)
    cl = now.replace(hour=15,minute=30,second=0)
    return o<=now<=cl, now.strftime("%H:%M IST")

# ─── FETCH ONE STOCK (runs in thread pool) ───────────────────
def fetch_one(sym, market, tf):
    """Fetch a single stock — called in parallel threads."""
    import time
    now = time.time()

    # Cache hit
    key = f"{sym}_{market}_{tf}"
    if key in cache and (now - cache_time.get(key,0)) < CACHE_TTL:
        return cache[key]

    try:
        ticker_sym = nse(sym) if market=="NSE" else sym
        period, interval = tf_params(tf)

        # Use yfinance batch download (faster than Ticker.history)
        df = yf.download(
            ticker_sym,
            period=period,
            interval=interval,
            progress=False,
            auto_adjust=True,
            threads=False,
        )
        if df is None or len(df) < 2: return None

        # Flatten columns if needed
        if isinstance(df.columns, pd.MultiIndex):
            df.columns = df.columns.get_level_values(0)

        last = df.iloc[-1]
        prev = df.iloc[-2]

        price  = round(float(last["Close"]), 2)
        open_  = round(float(last["Open"]),  2)
        high   = round(float(last["High"]),   2)
        low    = round(float(last["Low"]),    2)
        vol    = int(last["Volume"]) if not pd.isna(last["Volume"]) else 0
        prev_c = round(float(prev["Close"]),  2)
        chg    = round(((price-prev_c)/prev_c)*100, 2) if prev_c else 0

        rsi  = calc_rsi(df["Close"]) if len(df)>=15 else 50.0
        macd_v, macd_sig = calc_macd(df["Close"]) if len(df)>=26 else (0.0,0.0)

        # 52-week (use existing data if short tf)
        if tf in ("1d","1w"):
            df_1y = yf.download(ticker_sym,period="1y",interval="1d",progress=False,auto_adjust=True,threads=False)
            if isinstance(df_1y.columns, pd.MultiIndex): df_1y.columns=df_1y.columns.get_level_values(0)
        else:
            df_1y = df

        wk52h   = round(float(df_1y["High"].max()), 2)  if len(df_1y)>0 else high
        wk52l   = round(float(df_1y["Low"].min()),  2)  if len(df_1y)>0 else low
        vol_avg = int(df_1y["Volume"].mean())            if len(df_1y)>0 else vol

        result = {
            "symbol":   sym,
            "name":     sym,   # name resolved below if possible
            "price":    price,
            "open":     open_,
            "high":     high,
            "low":      low,
            "close":    price,
            "change":   chg,
            "volume":   vol,
            "vol_avg":  vol_avg,
            "rsi":      rsi,
            "macd":     macd_v,
            "macd_sig": macd_sig,
            "pe":       0.0,
            "div":      0.0,
            "wk52h":    wk52h,
            "wk52l":    wk52l,
            "sector":   SECTOR_MAP.get(sym,"Other"),
            "mcap":     MCAP_MAP.get(sym,"Mid"),
            "doji_score": doji_score(open_, price, high, low),
            "source":   "live",
        }

        cache[key]      = result
        cache_time[key] = now
        return result

    except Exception as e:
        print(f"[fetch] {sym}: {e}")
        return None

# ─── PARALLEL BATCH FETCH ────────────────────────────────────
def fetch_batch(symbols, market, tf, max_workers=10):
    """Fetch multiple stocks in parallel using thread pool."""
    from concurrent.futures import ThreadPoolExecutor, as_completed
    results = []
    with ThreadPoolExecutor(max_workers=max_workers) as ex:
        futures = {ex.submit(fetch_one, sym, market, tf): sym for sym in symbols}
        for future in as_completed(futures):
            try:
                r = future.result(timeout=15)
                if r: results.append(r)
            except Exception as e:
                print(f"[batch] {futures[future]}: {e}")
    return results

# ─── CRT PATTERN DETECTION ───────────────────────────────────
def detect_crt(sym, market, tf):
    d = fetch_one(sym, market, tf)
    if not d: return None
    ist = timezone(timedelta(hours=5,minutes=30))
    now = datetime.now(ist)
    h, m = now.hour, now.minute
    in_london  = 13 <= h < 17
    in_newyork = 18 <= h < 23
    ds = d["doji_score"]
    chg = d["change"]
    rsi = d["rsi"]
    bias, grade = None, "NO_TRADE"
    crt = False
    if chg > 0 and ds < 0.15:
        bias="bullish"; crt=True; grade="WEAK"
        if in_london or in_newyork: grade="VALID"
        if (in_london or in_newyork) and ds < 0.05: grade="A_PLUS"
    elif chg < 0 and ds < 0.15:
        bias="bearish"; crt=True; grade="WEAK"
        if in_london or in_newyork: grade="VALID"
        if (in_london or in_newyork) and ds < 0.05: grade="A_PLUS"
    d.update({"crt_bias": bias, "crt_grade": grade, "crt_detected": crt})
    return d

# ─── SCAN FILTERS ────────────────────────────────────────────
def passes_scan(d, scan_type):
    ds  = d.get("doji_score", 1)
    rsi = d.get("rsi", 50)
    chg = d.get("change", 0)
    vol = d.get("volume", 0)
    vav = d.get("vol_avg", 1)
    pe  = d.get("pe", 0)
    div = d.get("div", 0)
    mac = d.get("macd", 0)
    msi = d.get("macd_sig", 0)
    w5h = d.get("wk52h", 0)
    w5l = d.get("wk52l", 0)
    price = d.get("price", 0)
    h   = d.get("high", price)
    l   = d.get("low",  price)
    o   = d.get("open", price)
    rng = h - l
    hammer_score = (price - l) / rng if rng > 0 else 0
    star_score   = (h - price) / rng if rng > 0 else 0

    FILTERS = {
        "doji":           ds < 0.10,
        "hammer":         hammer_score > 0.65 and ds < 0.30,
        "shooting_star":  star_score   > 0.65 and ds < 0.30,
        "engulfing":      chg > 1.5 and o < price and ds > 0.5,
        "bear_engulf":    chg < -1.5 and o > price and ds > 0.5,
        "morning_star":   chg > 0 and rsi < 50 and ds < 0.3,
        "rsi_os":         rsi < 30,
        "rsi_ob":         rsi > 70,
        "macd_b":         mac > msi and mac > 0,
        "macd_br":        mac < msi and mac < 0,
        "stoch":          rsi < 25,   # proxy for stochastic
        "h52":            w5h > 0 and price/w5h > 0.95,
        "l52":            w5l > 0 and price/w5l < 1.05,
        "vsurge":         vav > 0 and vol > vav * 2,
        "emacx":          chg > 1.5 and vol > vav,
        "bbs":            abs(ds - 0.5) < 0.1,  # narrow body proxy
        "lowpe":          0 < pe < 15,
        "hidiv":          div > 2,
        "crt_aplus":      d.get("crt_grade") == "A_PLUS",
        "all":            True,
    }
    return FILTERS.get(scan_type, True)

# ─── ROUTES ──────────────────────────────────────────────────

@app.get("/")
def root():
    is_open, time_str = market_status()
    return {
        "status":      "LIVE",
        "version":     "3.0.0",
        "market_open": is_open,
        "ist_time":    time_str,
        "message":     "CRT Screener Backend — Fast Parallel Version",
    }

@app.get("/health")
def health():
    return {"ok": True}

@app.get("/scan")
def scan(
    type:      str   = Query("doji"),
    tf:        str   = Query("1d"),
    market:    str   = Query("NSE"),
    sector:    str   = Query("all"),
    min_price: float = Query(0),
    max_price: float = Query(9_999_999),
    min_rsi:   float = Query(0),
    max_rsi:   float = Query(100),
    min_vol:   float = Query(0),
    limit:     int   = Query(60),
):
    symbols = NSE_SYMBOLS if market == "NSE" else US_SYMBOLS
    symbols = symbols[:limit]

    # ── PARALLEL FETCH ──────────────────────────
    all_data = fetch_batch(symbols, market, tf, max_workers=10)

    # ── APPLY FILTERS ───────────────────────────
    results = []
    for d in all_data:
        if not passes_scan(d, type): continue
        if sector != "all" and d.get("sector") != sector: continue
        if not (min_price <= d["price"] <= max_price): continue
        if not (min_rsi   <= d["rsi"]   <= max_rsi):   continue
        if d["volume"] / 100_000 < min_vol:             continue
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

@app.get("/stock/{ticker}")
def stock_detail(ticker: str, market: str = Query("NSE")):
    d = fetch_one(ticker.upper(), market, "1d")
    if not d:
        return JSONResponse(status_code=404, content={"error": f"Could not fetch {ticker}"})
    return {"ok": True, "data": d}

@app.get("/quote")
def batch_quote(symbols: str = Query(...), market: str = Query("NSE")):
    syms = [s.strip().upper() for s in symbols.split(",")][:20]
    results = fetch_batch(syms, market, "1d", max_workers=8)
    quotes  = [{"symbol": d["symbol"], "price": d["price"], "change": d["change"]} for d in results]
    return {"ok": True, "quotes": quotes}

@app.get("/indices")
def indices():
    try:
        def get_index(sym):
            t = yf.Ticker(sym)
            h = t.history(period="2d")
            if h.empty: return None
            price  = round(float(h.iloc[-1]["Close"]), 2)
            prev   = round(float(h.iloc[-2]["Close"]), 2) if len(h) > 1 else price
            change = round(((price-prev)/prev)*100, 2)
            return {"price": price, "change": change}
        return {
            "nifty50":   get_index("^NSEI"),
            "sensex":    get_index("^BSESN"),
            "banknifty": get_index("^NSEBANK"),
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/crt/scan")
def crt_scan(
    tf:     str = Query("1d"),
    market: str = Query("NSE"),
    grade:  str = Query("all"),
    limit:  int = Query(50),
):
    symbols = (NSE_SYMBOLS if market == "NSE" else US_SYMBOLS)[:limit]

    # Fetch all in parallel first
    all_data = fetch_batch(symbols, market, tf, max_workers=10)

    # Apply CRT grading
    results = []
    ist = timezone(timedelta(hours=5, minutes=30))
    now = datetime.now(ist)
    h, m = now.hour, now.minute
    in_london  = 13 <= h < 17
    in_newyork = 18 <= h < 23

    for d in all_data:
        ds  = d.get("doji_score", 1)
        chg = d.get("change", 0)
        if abs(chg) < 0.3: continue  # skip flat

        bias  = "bullish" if chg > 0 else "bearish"
        crt_g = "WEAK"
        if in_london or in_newyork: crt_g = "VALID"
        if (in_london or in_newyork) and ds < 0.08: crt_g = "A_PLUS"

        if grade == "A_PLUS" and crt_g != "A_PLUS": continue
        if grade == "VALID"  and crt_g not in ("A_PLUS","VALID"): continue

        d["crt_bias"]     = bias
        d["crt_grade"]    = crt_g
        d["crt_detected"] = True
        results.append(d)

    results.sort(key=lambda x: {"A_PLUS":0,"VALID":1,"WEAK":2}.get(x["crt_grade"],3))

    return {
        "ok":      True,
        "scan":    "crt",
        "tf":      tf,
        "count":   len(results),
        "results": results,
    }

@app.get("/symbols")
def get_symbols():
    return {"ok": True, "symbols": NSE_SYMBOLS}
