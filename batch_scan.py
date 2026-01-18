from universe import NSE_200
from crt_logic import detect_crt

def scan_nse_200():
    results = []

    for symbol in NSE_200:
        try:
            crt = detect_crt(symbol)
            if crt:
                results.append({
                    "symbol": symbol,
                    "crt": crt
                })
        except Exception as e:
            print(f"Error scanning {symbol}: {e}")

    return {
        "scanned": len(NSE_200),
        "matches": results
    }
