from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from data import get_ohlc
from universe import NSE_200

app = FastAPI(
    title="CRT Screener Backend",
    version="1.0.0"
)

# -----------------------------
# CORS (important for Vercel)
# -----------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # you can restrict later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -----------------------------
# Health Check
# -----------------------------
@app.get("/")
def health():
    return {"status": "CRT Screener Backend Running"}

# -----------------------------
# Doji Logic
# -----------------------------
def is_doji(o, h, l, c):
    body = abs(c - o)
    range_ = h - l
    if range_ == 0:
        return False
    return body <= (range_ * 0.1)  # 10% body = doji

# -----------------------------
# Doji Screener (Chartink style)
# -----------------------------
@app.get("/screener/doji")
def doji_screener():
    results = []

    for symbol in NSE_200:
        try:
            df = get_ohlc(symbol)
            if df is None or len(df) == 0:
                continue

            last = df.iloc[-1]

            o = float(last["Open"])
            h = float(last["High"])
            l = float(last["Low"])
            c = float(last["Close"])

            if is_doji(o, h, l, c):
                results.append({
                    "symbol": symbol,
                    "open": round(o, 2),
                    "high": round(h, 2),
                    "low": round(l, 2),
                    "close": round(c, 2),
                })

        except Exception as e:
            print(f"Error in {symbol}: {e}")

    return results
