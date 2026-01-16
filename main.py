from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from scanner import scan_symbol  # your real CRT logic lives here

app = FastAPI(title="CRT Forex Screener")

# --- CORS (safe for frontend later) ---
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- FOREX UNIVERSE ---
FOREX_PAIRS = [
    "EURUSD=X",
    "GBPUSD=X",
    "USDJPY=X",
    "AUDUSD=X",
    "USDCHF=X",
    "USDCAD=X",
    "NZDUSD=X",
]

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "CRT Screener backend is live"
    }

@app.get("/scan")
def scan(tf: str = Query("daily", description="Timeframe: daily, 4h, 1h")):
    results = []

    for symbol in FOREX_PAIRS:
        try:
            crt_result = scan_symbol(symbol, tf)

            if crt_result is not None:
                results.append({
                    "symbol": symbol.replace("=X", ""),
                    "crt": crt_result["crt"],
                    "timeframe": tf
                })

        except Exception as e:
            # Prevent one symbol from killing the scan
            print(f"Error scanning {symbol}: {e}")

    return {
        "timeframe": tf,
        "total": len(results),
        "results": results
    }
