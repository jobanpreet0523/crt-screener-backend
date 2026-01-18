# batch_scan.py

from engine import run_single_scan

def run_batch_scan(symbols, timeframe):
    results = []

    for symbol in symbols:
        try:
            result = run_single_scan(symbol, timeframe)
            results.append(result)
        except Exception as e:
            results.append({
                "symbol": symbol,
                "error": str(e)
            })

    return results
