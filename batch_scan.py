from engine import run_single_scan
from symbols import get_symbols

def run_batch_scan(market="NIFTY", timeframe="15m", limit=200):
    symbols = get_symbols(market)[:limit]
    results = []

    for symbol in symbols:
        try:
            scan = run_single_scan(symbol, timeframe)
            if scan:
                results.append(scan)
        except Exception as e:
            print(f"Error scanning {symbol}: {e}")

    return results

