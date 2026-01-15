def is_crt(df):
    if len(df) < 5:
        return False

    ranges = []
    for i in range(5):
        high = df.iloc[-(i+1)]["High"]
        low = df.iloc[-(i+1)]["Low"]
        ranges.append(high - low)

    # Volatility contraction
    return ranges[0] < ranges[1] < ranges[2] < ranges[3]
