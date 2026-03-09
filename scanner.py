import yfinance as yf
from tickers import TICKERS

def doji_scan(tf):

    results=[]

    for ticker in TICKERS:

        try:

            if tf=="1d":
                interval="1d"
                period="10d"

            elif tf=="1w":
                interval="1wk"
                period="2y"

            elif tf=="1m":
                interval="1mo"
                period="5y"

            elif tf=="3m":
                interval="3mo"
                period="10y"

            else:
                return []

            df=yf.download(ticker,period=period,interval=interval,progress=False)

            if len(df)==0:
                continue

            last=df.iloc[-1]

            body=abs(last["Open"]-last["Close"])
            rng=last["High"]-last["Low"]

            if body<=rng*0.1:

                results.append({
                    "ticker":ticker,
                    "price":float(last["Close"])
                })

        except:
            continue

    return results
