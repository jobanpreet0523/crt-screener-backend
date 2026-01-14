from fastapi import Query, HTTPException
import yfinance as yf

@app.get("/scan")
def scan(tf: str = Query(..., description="daily, weekly, monthly")):

    tf_map = {
        "daily": "1d",
        "weekly": "1wk",
        "monthly": "1mo"
    }

    if tf not in tf_map:
        raise HTTPException(status_code=400, detail="Invalid timeframe")

    try:
        data = yf.download(
            tickers="AAPL MSFT TSLA",
            interval=tf_map[tf],
            period="6mo",
            group_by="ticker",
            progress=False
        )

        return {
            "status": "success",
            "timeframe": tf,
            "symbols": list(data.columns.levels[0])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


