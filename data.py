# data.py
import pandas as pd
from nsepython import equity_history

def get_ohlc(symbol: str, start: str, end: str) -> pd.DataFrame:
    """
    Fetch REAL NSE OHLC data
    symbol: RELIANCE, SBIN etc (NO .NS)
    start/end: YYYY-MM-DD
    """

    df = equity_history(
        symbol=symbol,
        series="EQ",
        start_date=start,
        end_date=end
    )

    if df.empty:
        return pd.DataFrame()

    df = df.rename(columns={
        "CH_TIMESTAMP": "date",
        "CH_OPENING_PRICE": "open",
        "CH_TRADE_HIGH_PRICE": "high",
        "CH_TRADE_LOW_PRICE": "low",
        "CH_CLOSING_PRICE": "close",
        "CH_TOT_TRADED_QTY": "volume"
    })

    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").reset_index(drop=True)

    return df[["date", "open", "high", "low", "close", "volume"]]
