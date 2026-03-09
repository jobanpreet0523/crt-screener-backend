import pandas as pd

def get_all_tickers():

    # NASDAQ stocks
    nasdaq = pd.read_csv(
        "https://raw.githubusercontent.com/datasets/nasdaq-listings/master/data/nasdaq-listed.csv"
    )

    # NYSE stocks
    nyse = pd.read_csv(
        "https://raw.githubusercontent.com/datasets/nyse-listed/master/data/nyse-listed.csv"
    )

    nasdaq_tickers = nasdaq["Symbol"].tolist()
    nyse_tickers = nyse["ACT Symbol"].tolist()

    tickers = list(set(nasdaq_tickers + nyse_tickers))

    return tickers
