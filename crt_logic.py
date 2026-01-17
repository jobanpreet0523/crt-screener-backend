def classify_crt(candles):
    """
    candles: list of dicts
    [
      {"open":..., "high":..., "low":..., "close":...},
      ...
    ]
    """

    if len(candles) < 5:
        return None

    impulse = candles[-3]
    range_candle = candles[-2]
    current = candles[-1]

    impulse_range = impulse["high"] - impulse["low"]
    body = abs(impulse["close"] - impulse["open"])

    # Ignore weak candles
    if body < impulse_range * 0.6:
        return None

    mid = impulse["low"] + impulse_range * 0.5

    # Bullish CRT
    if (
        impulse["close"] > impulse["open"]
        and range_candle["low"] >= impulse["low"]
        and current["close"] > mid
    ):
        return "Bullish"

    # Bearish CRT
    if (
        impulse["close"] < impulse["open"]
        and range_candle["high"] <= impulse["high"]
        and current["close"] < mid
    ):
        return "Bearish"

    return None
