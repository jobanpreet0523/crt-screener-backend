def get_us_stocks():
    """
    Returns a static list of highly liquid US stocks
    (safe for free Render + yfinance limits)
    """

    return [
        "AAPL", "MSFT", "GOOGL", "AMZN", "META",
        "NVDA", "TSLA", "NFLX", "AMD", "INTC",
        "JPM", "BAC", "WFC", "GS", "MS",
        "XOM", "CVX", "COP",
        "JNJ", "PFE", "MRK",
        "KO", "PEP", "WMT", "COST",
        "DIS", "NKE", "MCD",
        "BA", "CAT", "GE",
        "SPY", "QQQ", "DIA", "IWM",
        "PLTR", "COIN", "SQ", "PYPL",
        "SHOP", "UBER", "LYFT",
        "ABNB", "SNOW", "CRM"
    ]
