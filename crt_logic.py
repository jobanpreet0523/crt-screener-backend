# crt_logic.py

def is_volatility_contracting(df, bars=4):
    if df is None or len(df) < bars + 1:
        return False

    ranges = []
    for i in range(bars):
        candle = df.iloc[-(i+1)]
        high = candle["High"]
        low = candle["Low"]

        if high is None or low is None:
            return False

        ranges.append(high - low)

    return all(ranges[i] < ranges[i+1] for i in range(len(ranges) - 1))


def is_option_a(df):
    if not is_volatility_contracting(df):
        return False

    last = df.iloc[-1]
    mid = (last["High"] + last["Low"]) / 2
    return last["Close"] > mid


def is_option_b(df):
    if not is_volatility_contracting(df):
        return False

    last = df.iloc[-1]
    mid = (last["High"] + last["Low"]) / 2
    return last["Close"] < mid


def classify_crt(df):
    if df is None or df.empty:
        return None

    if is_option_a(df):
        return "OPTION_A_CONTINUATION"

    if is_option_b(df):
        return "OPTION_B_REVERSAL"

    return None
