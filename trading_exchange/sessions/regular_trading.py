import logging
from typing import Any

from trading_exchange.enums import EventTypeEnum
from trading_exchange.event import Event
from trading_exchange.order import Order
from trading_exchange.sessions.abstract_session import AbstractSession

_logger = logging.getLogger(__name__)


class RegularTrading(AbstractSession):

    def on_new_entry(self, entry: dict[str, Any]) -> list[Event]:
        _logger.debug(f"New entry received: {entry}")
        if entry["action"] == "NEW":
            return self._on_new_order(entry)
        return []


    def _on_new_order(self, entry: dict[str, Any]) -> list[Event]:
        _logger.debug("Process new order entity")

        events: list[Event] = []

        entry = self._normalize_entry(entry)
        order = Order.from_dict(entry)
        events.extend(self._check_for_trade(order))
        events.extend(self._add_new_order(order))

        return events

    def _normalize_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        entry["time_priority"] = self._orders_storage.get_order_time_priority
        _logger.debug(f"Normalized entry: {entry}")
        return entry

    def _check_for_trade(self, order: Order) -> list[Event]:
        return []

    def _add_new_order(self, order: Order) -> list[Event]:
        if order.leaves_qty > 0:
            self._orders_storage.add_order(order)
            return [Event(EventTypeEnum.ORDER_ADDED, order)]
        return []