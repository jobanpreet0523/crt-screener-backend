from symbols import NSE_SYMBOLS
from data_fetcher import get_ohlc
from crt_logic import detect_bullish_crt
from grader import grade_setup

def run_batch_scan():
    results = []

    for symbol in NSE_SYMBOLS:
        df = get_ohlc(symbol)

        crt = detect_bullish_crt(df)
        if not crt:
            continue

        grade = grade_setup(htf_bias="Bullish", liquidity="BSL")

        results.append({
            "symbol": symbol,
            **crt,
            "grade": grade
        })

    return results
