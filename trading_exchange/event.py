from dataclasses import dataclass
from typing import Any

from trading_exchange.enums import EventTypeEnum
from trading_exchange.order import Order


@dataclass(repr=True)
class Event:

    """
    Event class to store event information and type of event
    """

    event_type: EventTypeEnum
    info: dict[str, Any] or Order