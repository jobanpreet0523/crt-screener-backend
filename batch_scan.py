from universe import get_universe
from engine import run_scan   # only if this function EXISTS

def run_nse200_scan():
    symbols = get_universe()
    results = []

    for symbol in symbols:
        try:
            res = run_scan(symbol)
            if res:
                results.append(res)
        except Exception as e:
            print(f"Scan error {symbol}: {e}")

    return results
