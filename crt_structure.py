# crt_structure.py
# CRT Screener – HTF / LTF Structure Engine
# Role: Define market bias and structural confirmation

from typing import List, Literal, Dict
from statistics import mean

Bias = Literal["bullish", "bearish", "neutral"]
Candle = Dict[str, float]
