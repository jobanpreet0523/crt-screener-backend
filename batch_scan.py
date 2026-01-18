from universe import get_universe
from crt_logic import detect_crt
from data import get_ohlc   # must exist

def run_nse200_scan():
    results = []

    for symbol in get_universe():
        try:
            candles = get_ohlc(symbol, timeframe="1D")
            crt = detect_crt(candles)

            if crt:
                results.append({
                    "symbol": symbol,
                    "signal": crt["type"],
                    "base_high": crt["base_high"],
                    "base_low": crt["base_low"]
                })

        except Exception as e:
            print(f"Scan failed {symbol}: {e}")

    return results
