from crt_logic import classify_crt

def scan_symbol(symbol: str, interval: str):
    crt = classify_crt(symbol, interval)

    if not crt:
        return None

    return {
        "symbol": symbol,
        "crt": crt,
        "timeframe": interval
    }
