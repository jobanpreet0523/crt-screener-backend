def classify_crt(df):
    """
    Returns:
        OPTION_A_CONTINUATION
        OPTION_B_REVERSAL
        None
    """

    if df is None or len(df) < 6:
        return None

    try:
        # Last 5 candle ranges
        ranges = []
        for i in range(1, 6):
            high = df.iloc[-i]["High"]
            low = df.iloc[-i]["Low"]
            ranges.append(high - low)

        # Volatility contraction condition
        if not (ranges[0] < ranges[1] < ranges[2] < ranges[3]):
            return None

        # Direction logic
        last_close = df.iloc[-1]["Close"]
        prev_close = df.iloc[-2]["Close"]

        if last_close > prev_close:
            return "OPTION_A_CONTINUATION"
        else:
            return "OPTION_B_REVERSAL"

    except Exception:
        return None

