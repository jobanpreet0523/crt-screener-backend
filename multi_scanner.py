# multi_scanner.py
# Scan multiple symbols with CRT logic

from datetime import datetime
from typing import Dict, List

from crt_scanner import scan_crt_setup
from data_feed import DataFeed


def scan_markets(
    feed: DataFeed,
    symbols: Dict[str, Dict],
    timestamp: datetime | None = None
) -> List[Dict]:
    """
    symbols = {
        "EURUSD": {"htf": "1h", "ltf": "5m"},
        "NQ":     {"htf": "4h", "ltf": "5m"},
        "ES":     {"htf": "4h", "ltf": "5m"},
    }
    """
    if timestamp is None:
        timestamp = datetime.utcnow()

    results = []

    for symbol, tf in symbols.items():
        htf = feed.get_candles(symbol, tf["htf"], limit=200)
        ltf = feed.get_candles(symbol, tf["ltf"], limit=200)

        if not htf or not ltf:
            continue

        signal = scan_crt_setup(
            symbol=symbol,
            htf_candles=htf,
            ltf_candles=ltf,
            timestamp_utc=timestamp
        )

        results.append(signal)

    return results
