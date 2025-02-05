from typing import Any

import pytest

from trading_exchange.order import Order
from trading_exchange.orders_storage import OrdersStorage

@pytest.fixture(scope="module")
def target_order(order_data: dict[str, Any]) -> Order:
    return Order.from_dict(order_data)


def test_add_order_to_storage(orders_storage: OrdersStorage, target_order: Order) -> None:
    orders_storage.add_order(target_order)

    assert target_order in orders_storage.get_all_orders, "Order is not in the storage"


def test_remove_order_from_storage(orders_storage: OrdersStorage, target_order: Order) -> None:
    orders_storage.add_order(target_order)
    orders_storage.remove_order_by_id(target_order.id)

    assert target_order not in orders_storage.get_all_orders, "Order is still in the storage"


def test_get_order_by_id(orders_storage: OrdersStorage, target_order: Order) -> None:
    orders_storage.add_order(target_order)
    order = orders_storage.get_order_by_id(target_order.id)

    assert order == target_order, "Order is not the same as the target order"