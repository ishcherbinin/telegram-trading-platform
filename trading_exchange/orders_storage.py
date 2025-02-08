import logging
from typing import Optional

from trading_exchange.order import Order

_logger = logging.getLogger(__name__)


class OrdersStorage:

    """
    Class to store orders in the exchange. It provides methods to add, remove and get orders by id.
    It cannot update or modify orders, only remove them.
    """


    def __init__(self):
        self._orders: list[Order] = []

    def __repr__(self) -> str:
        return f"OrdersStorage(orders={self._orders})"

    def add_order(self, order: Order) -> None:
        self._orders.append(order)
        _logger.debug(f"Order {order.id} added to storage")

    def remove_order_by_id(self, order_id: str) -> None:
        target_order = self.get_order_by_id(order_id)
        if target_order:
            self._orders.remove(target_order)
            _logger.debug(f"Order {order_id} removed from storage")

    def get_order_by_id(self, order_id: str) -> Optional[Order]:
        return next(filter(lambda order: order.id == order_id, self._orders), None)

    def get_orders_by_username(self, username: str) -> tuple[Order, ...]:
        return tuple(order for order in self._orders if order.username == username)

    def clear_terminated_orders(self) -> None:
        self._orders = [order for order in self._orders if order.leaves_qty > 0]

    @property
    def get_order_time_priority(self) -> int:
        return len(self._orders)

    @property
    def get_all_orders(self) -> list[Order]:
        return self._orders

    @property
    def get_next_order_id(self) -> int:
        return len(self._orders) + 1