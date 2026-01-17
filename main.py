from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from scanner import scan_symbol
from universe import get_symbols
from tf_map import TF_MAP

app = FastAPI(title="CRT Screener Backend")

# --------------------
# CORS
# --------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# --------------------
# Health Check
# --------------------
@app.get("/")
def root():
    return {
        "status": "OK",
        "service": "CRT Screener Backend"
    }

# --------------------
# Scan Endpoint
# --------------------
@app.get("/scan")
def scan(tf: str = Query("daily", description="Timeframe")):
    tf = tf.lower()

    if tf not in TF_MAP:
        return {
            "error": "Invalid timeframe",
            "allowed": list(TF_MAP.keys())
        }

    interval = TF_MAP[tf]

    symbols = get_symbols()
    results = []

    for symbol in symbols:
        try:
            res = scan_symbol(symbol, interval)
            if res:
                results.append(res)
        except Exception as e:
            print(f"Error scanning {symbol}: {e}")

    return {
        "timeframe": tf,
        "total": len(results),
        "results": results
    }
