# batch_scan.py

from universe import NSE_200
from data import get_ohlc
from crt_logic import detect_crt


def run_nse200_scan():
    results = []

    for symbol in NSE_200:
        try:
            df = get_ohlc(symbol)

            if detect_crt(df):
                results.append({
                    "symbol": symbol,
                    "timeframe": "1D",
                    "setup": "CRT"
                })

        except Exception as e:
            continue  # never break batch scan

    return results
