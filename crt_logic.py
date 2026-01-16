def detect_crt(symbol, tf):
    """
    Returns:
    - 'Bullish'
    - 'Bearish'
    - None
    """

    # Example structural filters (not easy logic)
    liquidity_taken = True
    displacement = True
    range_respected = tf in ["daily", "4h"]

    if liquidity_taken and displacement and range_respected:
        return "Bullish"

    return None
