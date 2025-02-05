"""
This module contains all the enums used in the trading exchange.
"""
from enum import Enum


class SideEnum(Enum):

    BUY = "BUY"
    SELL = "SELL"

class OrderStatusEnum(Enum):

    NEW = "NEW"
    PARTIALLY_FILLED = "PARTIALLY_FILLED"
    FILLED = "FILLED"
    CANCELED = "CANCELED"
    REJECTED = "REJECTED"

class EventTypeEnum(Enum):

    ORDER_ADDED = "ORDER_ADDED"
    ORDER_CANCELED = "ORDER_CANCELED"
    ORDER_TRADED = "ORDER_TRADED"
