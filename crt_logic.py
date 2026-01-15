# crt_logic.py

def is_crt(df):
    if len(df) < 5:
        return False

    ranges = []
    for i in range(5):
        high = df.iloc[-(i+1)]["High"]
        low = df.iloc[-(i+1)]["Low"]
        ranges.append(high - low)

    # Volatility contraction
   return ranges[0] < ranges[1] and ranges[1] < ranges[2]



def classify_crt(df):
    if is_option_a(df):
        return "OPTION_A_CONTINUATION"
    if is_option_b(df):
        return "OPTION_B_REVERSAL"
    return None

