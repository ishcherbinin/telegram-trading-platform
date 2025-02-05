from abc import ABC, abstractmethod
from typing import Any

from trading_exchange.event import Event
from trading_exchange.orders_storage import OrdersStorage


class AbstractSession(ABC):
    """
    Abstract class for session. Defines strategy for creating other sessions
    """

    def __init__(self, orders_storage: OrdersStorage):
        self._orders_storage = orders_storage

    def __repr__(self):
        return f"Logic for {self.__class__.__name__}"

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def on_session_start(self, session_change_request: dict[str, Any]) -> list[Event]:
        """
        Method performs actions on session start
        :param session_change_request: request values
        :return:
        """
        return []

    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def on_session_end(self, session_change_request: dict[str, Any]) -> list[Event]:
        """
        Method performs actions on session end
        :param session_change_request: request values
        :return:
        """
        return []

    # noinspection PyMethodMayBeStatic
    @abstractmethod
    def on_new_entry(self, entry: dict[str, Any]) -> list[Event]:
        """
        Method performs actions on new entry.
        :param entry: entry values
        :return:
        """
        pass