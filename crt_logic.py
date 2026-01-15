def classify_crt(df):
    """
    CRT Classification:
    OPTION_A_CONTINUATION → contraction in trend direction
    OPTION_B_REVERSAL     → contraction against trend
    """

    if df is None or len(df) < 10:
        returns: None

    try:
        # -----------------------------
        # 1️⃣ Volatility contraction (last 5 candles)
        # -----------------------------
        ranges = []
        bodies = []

        for i in range(1, 6):
            high = df.iloc[-i]["High"]
            low = df.iloc[-i]["Low"]
            open_ = df.iloc[-i]["Open"]
            close = df.iloc[-i]["Close"]

            ranges.append(high - low)
            bodies.append(abs(close - open_))

        # Contraction condition (flexible, realistic)
        if not (
            ranges[0] < ranges[1] and
            ranges[1] <= ranges[2] and
            ranges[2] <= ranges[3]
        ):
            return None

        if not (
            bodies[0] < bodies[1] and
            bodies[1] <= bodies[2]
        ):
            return None

        # -----------------------------
        # 2️⃣ Trend before contraction (5–10 candles back)
        # -----------------------------
        prev_close = df.iloc[-6]["Close"]
        prev_prev_close = df.iloc[-10]["Close"]

        if prev_close > prev_prev_close:
            trend = "UP"
        elif prev_close < prev_prev_close:
            trend = "DOWN"
        else:
            return None

        # -----------------------------
        # 3️⃣ CRT Type classification
        # -----------------------------
        last_close = df.iloc[-1]["Close"]
        last_open = df.iloc[-1]["Open"]

        if trend == "UP" and last_close > last_open:
            return "OPTION_A_CONTINUATION"

        if trend == "DOWN" and last_close < last_open:
            return "OPTION_A_CONTINUATION"

        return "OPTION_B_REVERSAL"

    except Exception:
        return None
