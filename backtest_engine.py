# backtest_engine.py
import pandas as pd

def backtest_long(df: pd.DataFrame):
    """
    Simple CRT-style backtest:
    - Entry: Close breaks previous high
    - SL: Previous candle low
    - Target: 2R
    """

    trades = []

    for i in range(2, len(df)):
        prev = df.iloc[i - 1]
        curr = df.iloc[i]

        if curr["close"] > prev["high"]:
            entry = curr["close"]
            stop = prev["low"]
            risk = entry - stop
            target = entry + (2 * risk)

            result = "OPEN"

            for j in range(i + 1, len(df)):
                candle = df.iloc[j]

                if candle["low"] <= stop:
                    result = "LOSS"
                    exit_price = stop
                    break
                elif candle["high"] >= target:
                    result = "WIN"
                    exit_price = target
                    break
            else:
                continue

            trades.append({
                "entry_date": curr["date"],
                "entry": entry,
                "stop": stop,
                "target": target,
                "exit": exit_price,
                "result": result
            })

    return pd.DataFrame(trades)
