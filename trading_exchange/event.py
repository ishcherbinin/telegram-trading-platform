from dataclasses import dataclass
from typing import Any, Union

from trading_exchange.enums import EventTypeEnum
from trading_exchange.order import Order
from trading_exchange.trade import Trade


@dataclass(repr=True)
class Event:

    """
    Event class to store event information and type of event
    """

    event_type: EventTypeEnum
    info: Union[dict[str, Any], Order, Trade]