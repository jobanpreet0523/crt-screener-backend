import yfinance as yf
from crt_logic import classify_crt


def scan_symbol(symbol: str, interval: str):
    try:
        df = yf.download(
            symbol,
            period="3mo",
            interval=interval,
            progress=False
        )

        if df.empty or len(df) < 10:
            return None

        candles = []
        for _, row in df.iterrows():
            candles.append({
                "open": float(row["Open"]),
                "high": float(row["High"]),
                "low": float(row["Low"]),
                "close": float(row["Close"]),
            })

        crt = classify_crt(candles)

        if not crt:
            return None

        return {
            "symbol": symbol,
            "crt": crt
        }

    except Exception as e:
        return None
