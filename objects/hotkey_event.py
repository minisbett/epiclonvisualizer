from typing import TypedDict
from datetime import datetime


class HotkeyEvent(TypedDict):
    hotkey: str
    timestamp: datetime
