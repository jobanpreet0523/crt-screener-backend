from fastapi import FastAPI, Query
from universe import get_forex_pairs

app = FastAPI()

@app.get("/")
def root():
    return {
        "status": "ok",
        "message": "CRT Screener backend is live"
    }


@app.get("/scan")
def scan(tf: str = Query("daily")):
    symbols = get_forex_pairs()
    results = []

    for symbol in symbols:
        crt_bias = detect_crt(symbol, tf)

        if crt_bias is not None:
            results.append({
                "symbol": symbol,
                "crt": crt_bias,
                "timeframe": tf
            })

    return {
        "timeframe": tf,
        "total": len(results),
        "results": results
    }
