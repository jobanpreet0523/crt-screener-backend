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

    print("========== SCAN START ==========")
    print("Timeframe:", tf)
    print("Total symbols:", len(symbols))

    for symbol in symbols:
        print(f"Scanning {symbol}...")

        crt_bias = detect_crt(symbol, tf)

        print(f"Result for {symbol}: {crt_bias}")

        if crt_bias is not None:
            results.append({
                "symbol": symbol,
                "crt": crt_bias,
                "timeframe": tf
            })

    print("========== SCAN END ==========")

    return {
        "timeframe": tf,
        "total": len(results),
        "results": results
    }
def detect_crt(symbol, tf):
    print(f" → detect_crt() called for {symbol} on {tf}")

    liquidity_taken = True
    displacement = True
    valid_tf = tf in ["daily", "4h"]

    print(
        f"   liquidity_taken={liquidity_taken}, "
        f"displacement={displacement}, "
        f"valid_tf={valid_tf}"
    )

    if liquidity_taken and displacement and valid_tf:
        return "Bullish"

    return None
