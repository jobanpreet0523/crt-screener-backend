def scan_symbol(symbol: str, interval: str):
    # Your real CRT logic is here
    # Must return None OR a dict

    crt_signal = detect_crt(symbol, interval)  # your logic

    if not crt_signal:
        return None

    return {
        "symbol": symbol,
        "crt": crt_signal,
        "timeframe": interval
    }
