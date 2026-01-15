def is_option_a(df):
    """
    OPTION A: CRT CONTINUATION
    - Volatility contraction
    - Trend continuation structure
    """

    if len(df) < 6:
        return False

    last = df.iloc[-1]
    prev = df.iloc[-2]

    # Candle ranges (last 4 candles)
    ranges = []
    for i in range(1, 5):
        candle = df.iloc[-i]
        ranges.append(candle["High"] - candle["Low"])

    # Volatility contraction
    if not (ranges[0] < ranges[1] < ranges[2] < ranges[3]):
        return False

    # Bullish continuation logic
    if last["Close"] <= prev["Close"]:
        return False

    return True


def is_option_b(df):
    """
    OPTION B: CRT REVERSAL
    - Compression after selloff
    - Reversal intent candle
    """

    if len(df) < 6:
        return False

    last = df.iloc[-1]
    prev = df.iloc[-2]
    prev2 = df.iloc[-3]

    # Compression candles
    ranges = []
    for i in range(1, 5):
        candle = df.iloc[-i]
        ranges.append(candle["High"] - candle["Low"])

    if not (ranges[0] < ranges[1] < ranges[2]):
        return False

    # Reversal conditions
    if last["Close"] <= last["Open"]:
        return False

    if last["Close"] <= prev2["Low"]:
        return False

    return True


def classify_crt(df):
    if is_option_a(df):
        return "OPTION_A_CONTINUATION"

    if is_option_b(df):
        return "OPTION_B_REVERSAL"

    return None
