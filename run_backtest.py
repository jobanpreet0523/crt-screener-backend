from universe import NSE_200
from data import get_ohlc
from backtest_engine import backtest_long

START = "2022-01-01"
END = "2025-01-01"

summary = []

for symbol in NSE_200:
    print(f"Backtesting {symbol}...")

    df = get_ohlc(symbol, START, END)
    if df.empty or len(df) < 100:
        continue

    trades = backtest_long(df)
    if trades.empty:
        continue

    wins = len(trades[trades["result"] == "WIN"])
    losses = len(trades[trades["result"] == "LOSS"])

    summary.append({
        "symbol": symbol,
        "trades": len(trades),
        "wins": wins,
        "losses": losses,
        "winrate": round((wins / len(trades)) * 100, 2)
    })

print(summary)
