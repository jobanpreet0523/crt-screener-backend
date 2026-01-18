from scanner.engine import run_single_scan

def run_batch_scan(market="NIFTY", timeframe="15m", limit=200):
    symbols = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS"
        # later we auto-load 200 NSE stocks
    ]

    results = []

    for symbol in symbols[:limit]:
        data = run_single_scan(symbol, timeframe)
        if data:
            results.append(data)

    return results
