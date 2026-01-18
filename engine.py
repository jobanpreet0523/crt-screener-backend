def backtest_crt(df):
    trades = []

    for i in range(20, len(df)):
        window = df.iloc[i-20:i]

        crt = detect_bullish_crt(window)
        if not crt:
            continue

        entry = crt["entry"]
        sl = crt["sl"]
        target = entry + (entry - sl) * 2

        outcome = simulate_trade(df.iloc[i:], entry, sl, target)

        trades.append({
            "entry": entry,
            "sl": sl,
            "target": target,
            "result": outcome
        })

    return trades
