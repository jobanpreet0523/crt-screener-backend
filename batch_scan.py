from symbols import NSE_SYMBOLS
from engine import run_single_scan

def run_batch_scan():
    results = []
    for symbol in NSE_SYMBOLS:
        scan = run_single_scan(symbol, "15m")
        if scan:
            results.append(scan)
    return results
