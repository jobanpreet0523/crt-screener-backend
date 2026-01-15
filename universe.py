import pandas as pd

def get_us_stocks():
    url = "https://datahub.io/core/nasdaq-listings/r/nasdaq-listed-symbols.csv"
    df = pd.read_csv(url)
    return df["Symbol"].tolist()
