def calculate_metrics(trades):
    wins = sum(1 for t in trades if t["result"] == "WIN")
    losses = sum(1 for t in trades if t["result"] == "LOSS")

    winrate = wins / max(1, (wins + losses))

    return {
        "total_trades": len(trades),
        "wins": wins,
        "losses": losses,
        "winrate": round(winrate * 100, 2)
    }
