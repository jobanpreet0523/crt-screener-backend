# markets.py
# CRT Screener – Market Definitions
# Author: CRT System
# Role: Central instrument + session registry

from dataclasses import dataclass
from typing import Dict, List


# ─────────────────────────────────────────────
# Core Market Structure
# ─────────────────────────────────────────────

@dataclass
class Market:
    symbol: str
    name: str
    market_type: str   # Forex | Index | Future
    session: str       # Asia | London | NewYork | CME
    tick_size: float
    contract_size: float | None = None


# ─────────────────────────────────────────────
# FOREX MARKETS
# ─────────────────────────────────────────────

FOREX_MARKETS: Dict[str, Market] = {
    "EURUSD": Market(
        symbol="EURUSD",
        name="Euro / US Dollar",
        market_type="Forex",
        session="London",
        tick_size=0.00001
    ),
    "GBPUSD": Market(
        symbol="GBPUSD",
        name="British Pound / US Dollar",
        market_type="Forex",
        session="London",
        tick_size=0.00001
    ),
    "USDJPY": Market(
        symbol="USDJPY",
        name="US Dollar / Japanese Yen",
        market_type="Forex",
        session="Asia",
        tick_size=0.001
    )
}


# ─────────────────────────────────────────────
# INDICES
# ─────────────────────────────────────────────

INDICES_MARKETS: Dict[str, Market] = {
    "NAS100": Market(
        symbol="NAS100",
        name="NASDAQ 100",
        market_type="Index",
        session="NewYork",
        tick_size=0.25
    ),
    "SPX500": Market(
        symbol="SPX500",
        name="S&P 500",
        market_type="Index",
        session="NewYork",
        tick_size=0.25
    ),
    "US30": Market(
        symbol="US30",
        name="Dow Jones 30",
        market_type="Index",
        session="NewYork",
        tick_size=1.0
    )
}


# ─────────────────────────────────────────────
# FUTURES (CME)
# ─────────────────────────────────────────────

FUTURES_MARKETS: Dict[str, Market] = {
    "ES": Market(
        symbol="ES",
        name="E-mini S&P 500",
        market_type="Future",
        session="CME",
        tick_size=0.25,
        contract_size=50
    ),
    "NQ": Market(
        symbol="NQ",
        name="E-mini NASDAQ",
        market_type="Future",
        session="CME",
        tick_size=0.25,
        contract_size=20
    ),
    "GC": Market(
        symbol="GC",
        name="Gold Futures",
        market_type="Future",
        session="CME",
        tick_size=0.1,
        contract_size=100
    )
}


# ─────────────────────────────────────────────
# Combined Access Layer
# ─────────────────────────────────────────────

ALL_MARKETS: Dict[str, Market] = {
    **FOREX_MARKETS,
    **INDICES_MARKETS,
    **FUTURES_MARKETS
}


def get_market(symbol: str) -> Market:
    """Return market object by symbol"""
    symbol = symbol.upper()
    if symbol not in ALL_MARKETS:
        raise ValueError(f"Market {symbol} not supported")
    return ALL_MARKETS[symbol]


def list_markets(market_type: str | None = None) -> List[Market]:
    """List markets optionally filtered by type"""
    if market_type is None:
        return list(ALL_MARKETS.values())
    return [
        m for m in ALL_MARKETS.values()
        if m.market_type.lower() == market_type.lower()
    ]
