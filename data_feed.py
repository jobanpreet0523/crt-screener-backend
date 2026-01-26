# data_feed.py
# CRT Screener – Unified Data Feed Layer
# Role: Normalize candle data from any source

from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Dict
import pandas as pd


Candle = Dict[str, float | datetime]


# ─────────────────────────────────────────────
# Abstract Base Feed
# ─────────────────────────────────────────────

class DataFeed(ABC):
    """
    Base class for all data feeds.
    Every feed MUST return candles in CRT format.
    """

    @abstractmethod
    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 200
    ) -> List[Candle]:
        pass


# ─────────────────────────────────────────────
# REST / CSV / BACKTEST FEED
# ─────────────────────────────────────────────

class RestDataFeed(DataFeed):
    """
    Generic REST / CSV / historical feed
    """

    def __init__(self, source: str):
        """
        source = path to CSV or future REST endpoint
        """
        self.source = source

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 200
    ) -> List[Candle]:

        df = pd.read_csv(self.source)

        df = df.tail(limit)

        candles = []
        for _, row in df.iterrows():
            candles.append({
                "time": pd.to_datetime(row["time"]),
                "open": float(row["open"]),
                "high": float(row["high"]),
                "low": float(row["low"]),
                "close": float(row["close"]),
                "volume": float(row.get("volume", 0))
            })

        return candles


# ─────────────────────────────────────────────
# MT5 DATA FEED (FOREX)
# ─────────────────────────────────────────────

class MT5DataFeed(DataFeed):
    """
    Placeholder for MetaTrader 5 integration
    """

    def __init__(self):
        try:
            import MetaTrader5 as mt5
            self.mt5 = mt5
            if not self.mt5.initialize():
                raise RuntimeError("MT5 initialization failed")
        except ImportError:
            raise ImportError("MetaTrader5 package not installed")

    def get_candles(
        self,
        symbol: str,
        timeframe: str,
        limit: int = 200
    ) -> List[Candle]:

        tf_map = {
            "1m": self.mt5.TIMEFRAME_M1,
            "5m": self.mt5.TIMEFRAME_M5,
            "15m": self.mt5.TIMEFRAME_M15,
            "1h": self.mt5.TIMEFRAME_H1,
            "4h": self.mt5.TIMEFRAME_H4,
            "1d": self.mt5.TIMEFRAME_D1,
        }

        rates = self.mt5.copy_rates_from_pos(
            symbol,
            tf_map[timeframe],
            0,
            limit
        )

        candles = []
        for r in rates:
