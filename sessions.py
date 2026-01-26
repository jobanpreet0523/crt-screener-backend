# sessions.py
# CRT Screener – Session & Killzone Engine
# Role: Time-based execution filter

from datetime import datetime, time
from typing import Literal
import pytz


SessionName = Literal["Asia", "London", "NewYork", "Off"]


# ─────────────────────────────────────────────
# Timezone Definitions
# ─────────────────────────────────────────────

UTC = pytz.utc
LONDON_TZ = pytz.timezone("Europe/London")
NEWYORK_TZ = pytz.timezone("America/New_York")
ASIA_TZ = pytz.timezone("Asia/Tokyo")


# ─────────────────────────────────────────────
# Killzone Definitions (LOCAL TIMES)
# ─────────────────────────────────────────────
# These are industry-standard CRT windows

ASIA_SESSION = {
    "start": time(0, 0),
    "end": time(6, 0),
}

LONDON_KILLZONE = {
    "start": time(7, 0),
    "end": time(10, 0),
}

NEWYORK_KILLZONE = {
    "start": time(13, 0),
    "end": time(16, 0),
}


# ─────────────────────────────────────────────
# Core Session Detection
# ─────────────────────────────────────────────

def _is_time_between(t: time, start: time, end: time) -> bool:
    """Check if time t is between start and end"""
    return start <= t <= end


def get_current_session(
    now: datetime | None = None
) -> SessionName:
    """
    Determine current market session (CRT logic)
    """
    if now is None:
        now = datetime.utcnow().replace(tzinfo=UTC)

    london_time = now.astimezone(LONDON_TZ).time()
    ny_time = now.astimezone(NEWYORK_TZ).time()
    asia_time = now.astimezone(ASIA_TZ).time()

    if _is_time_between(london_time, **LONDON_KILLZONE):
        return "London"

    if _is_time_between(ny_time, **NEWYORK_KILLZONE):
        return "NewYork"

    if _is_time_between(asia_time, **ASIA_SESSION):
        return "Asia"

    return "Off"


# ─────────────────────────────────────────────
# CRT Execution Filter
# ─────────────────────────────────────────────

def is_execution_window(
    required_session: SessionName,
    now: datetime | None = None
) -> bool:
    """
    Check if we are inside the required CRT session
    """
    current = get_current_session(now)
    return current == required_session


# ─────────────────────────────────────────────
# Convenience Helpers
# ─────────────────────────────────────────────

def allow_a_plus(
    market_session: SessionName,
    now: datetime | None = None
) -> bool:
    """
    A+ signals are ONLY allowed during
    London or New York sessions
    """
    current = get_current_session(now)

    if market_session in ("London", "NewYork"):
        return current == market_session

    return False
