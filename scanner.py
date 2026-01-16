import yfinance as yf
from crt_logic import classify_crt

def scan_symbol(symbol: str, interval: str):
    try:
        df = yf.download(
            symbol,
            interval=interval,
            period="6mo",
            progress=False
        )

        if df is None or df.empty:
            return None

        crt = classify_crt(df)

        if crt:
            return {
                "symbol": symbol,
                "crt": crt
            }

    except Exception:
        return None

    return None
