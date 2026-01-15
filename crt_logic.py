# crt_logic.py

def is_volatility_contracting(df, bars=4):
    if len(df) < bars + 1:
        return False

    ranges = []
    for i in range(bars):
        high = df.iloc[-(i+1)]["High"]
        low = df.iloc[-(i+1)]["Low"]
        ranges.append(high - low)

    # STRICT contraction: newest < previous < older
    return all(ranges[i] < ranges[i+1] for i in range(len(ranges) - 1))


def is_option_a(df):
    """
    OPTION A: Continuation CRT
    - Volatility contracting
    - Close near highs
    """
    if not is_volatility_contracting(df):
        return False

    last = df.iloc[-1]
    return last["Close"] > (last["High"] + last["Low"]) / 2


def is_option_b(df):
    """
    OPTION B: Reversal CRT
    - Volatility contracting
    - Close near lows
    """
    if not is_volatility_contracting(df):
        return False

    last = df.iloc[-1]
    return last["Close"] < (last["High"] + last["Low"]) / 2


def classify_crt(df):
    if is_option_a(df):
        return "OPTION_A_CONTINUATION"

    if is_option_b(df):
        return "OPTION_B_REVERSAL"

    return None
