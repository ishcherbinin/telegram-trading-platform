from typing import Any

from trading_exchange.event import Event
from trading_exchange.orders_storage import OrdersStorage
from trading_exchange.sessions.regular_trading import RegularTrading


def test_adding_new_order(
        regular_trading: RegularTrading,
        orders_storage: OrdersStorage,
        new_entry: dict[str, Any]) -> None:

    events: list[Event] = regular_trading.on_new_entry(new_entry)

    assert len(events) == 1, "Event was not generated"

    event = events[0]

    assert event.event_type.value == "ORDER_ADDED", "Event type is not 'ORDER_ADDED'"

    assert len(orders_storage.get_all_orders) == 1, "Order was not added to the storage"

    order = orders_storage.get_order_by_id(new_entry["id"])

    assert order is not None, "Order was not added to the storage"
    assert order.status.value == "NEW", "Order status is not 'NEW'"



