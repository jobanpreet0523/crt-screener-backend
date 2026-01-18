# crt_logic.py

def detect_crt(df):
    """
    Simple CRT logic:
    - Compression (lower range)
    - Break structure potential
    """

    if df is None or len(df) < 20:
        return False

    recent = df.tail(10)

    high_range = recent["High"].max()
    low_range = recent["Low"].min()

    compression = (high_range - low_range) / low_range < 0.03  # <3%

    return compression
