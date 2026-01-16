@app.get("/scan")
def scan(tf: str = "daily", demo: bool = False):
    # 🔹 DEMO MODE (for testing frontend)
    if demo:
        results = [
            {
                "symbol": "EURUSD",
                "crt": "Bullish",
                "timeframe": tf
            },
            {
                "symbol": "USDJPY",
                "crt": "Bearish",
                "timeframe": tf
            }
        ]

        return {
            "timeframe": tf,
            "total": len(results),
            "results": results
        }

    # 🔹 REAL SCAN MODE
    tf_map = {
        "daily": "1d",
        "4h": "4h",
        "1h": "1h"
    }

    interval = tf_map.get(tf)
    if not interval:
        return {"error": "Invalid timeframe"}

    symbols = get_us_stocks()[:200]
    results = []

    for symbol in symbols:
        res = scan_symbol(symbol, interval)
        if res:
            results.append(res)

    return {
        "timeframe": tf,
        "total": len(results),
        "results": results
    }
