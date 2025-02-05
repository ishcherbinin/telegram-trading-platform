from dataclasses import dataclass
from typing import Any

from trading_exchange.enums import EventTypeEnum
from trading_exchange.order import Order


@dataclass(repr=True)
class Event:

    event_type: EventTypeEnum
    info: dict[str, Any] or Order