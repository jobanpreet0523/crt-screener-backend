import pandas as pd


def validate_df(df):
    if df is None:
        return False

    if not isinstance(df, pd.DataFrame):
        return False

    if df.shape[0] < 6:
        return False

    required_cols = {"Open", "High", "Low", "Close"}
    if not required_cols.issubset(set(df.columns)):
        return False

    return True


def is_option_a(df):
    # OPTION A: Continuation CRT

    if not validate_df(df):
        return False

    last = df.iloc[-1]
    prev = df.iloc[-2]

    ranges = []
    for i in range(1, 5):
        candle = df.iloc[-i]
        ranges.append(float(candle["High"] - candle["Low"]))

    # Volatility contraction
    if not (ranges[0] < ranges[1] < ranges[2] < ranges[3]):
        return False

    # Bullish continuation
    if float(last["Close"]) <= float(prev["Close"]):
        return False

    return True


def is_option_b(df):
    # OPTION B: Reversal CRT

    if not validate_df(df):
        return False

    last = df.iloc[-1]
    prev2 = df.iloc[-3]

    ranges = []
    for i in range(1, 4):
        candle = df.iloc[-i]
        ranges.append(float(candle["High"] - candle["Low"]))

    if not (ranges[0] < ranges[1] < ranges[2]):
        return False

    # Bullish reversal intent
    if float(last["Close"]) <= float(last["Open"]):
        return False

    if float(last["Close"]) <= float(prev2["Low"]):
        return False

    return True


def classify_crt(df):
    try:
        if is_option_a(df):
            return "OPTION_A_CONTINUATION"

        if is_option_b(df):
            return "OPTION_B_REVERSAL"

    except Exception as e:
        return None

    return None
