from typing import Any

import pytest

from trading_exchange.event import Event
from trading_exchange.orders_storage import OrdersStorage
from trading_exchange.sessions.regular_trading import RegularTrading

@pytest.fixture
def contra_entry(new_entry: dict[str, Any]) -> dict[str, Any]:
    contra_entry = new_entry.copy()
    contra_entry["side"] = "SELL"
    contra_entry["id"] = "124"
    contra_entry["username"] = "contra_user"
    return contra_entry



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

def test_two_orders_fully_traded(
        regular_trading: RegularTrading,
        orders_storage: OrdersStorage,
        contra_entry: dict[str, Any],
        new_entry: dict[str, Any]):

    regular_trading.on_new_entry(new_entry)

    events = regular_trading.on_new_entry(contra_entry)

    new_events = tuple(event for event in events if event.event_type.value == "ORDER_ADDED")

    trd_events = tuple(event for event in events if event.event_type.value == "ORDER_TRADED")

    assert len(trd_events) == 2, "Trade events were not generated"

    assert len(new_events) == 0, "Event new incorrectly generated for any of orders"

    assert len(orders_storage.get_all_orders) == 0, "Orders were not removed from the storage"

def test_part_traded_flow(
        regular_trading: RegularTrading,
        orders_storage: OrdersStorage,
        contra_entry: dict[str, Any],
        new_entry: dict[str, Any]):
    regular_trading.on_new_entry(new_entry)

    contra_entry["order_qty"] += 5

    events = regular_trading.on_new_entry(contra_entry)

    new_events = tuple(event for event in events if event.event_type.value == "ORDER_ADDED")

    trd_events = tuple(event for event in events if event.event_type.value == "ORDER_TRADED")

    assert len(trd_events) == 2, "Trade events were not generated"

    assert len(new_events) == 1, "Event new was not generated for contra order"

    contra_order = orders_storage.get_order_by_id(contra_entry["id"])

    assert contra_order is not None, "Contra order was not added to the storage"

    assert contra_order.leaves_qty == 5, "Contra order was not updated"

    assert len(orders_storage.get_all_orders) == 1, "Orders were not removed from the storage"



def test_cancel_flow(
        regular_trading: RegularTrading,
        orders_storage: OrdersStorage,
        new_entry: dict[str, Any],
        cancel_entry: dict[str, Any]):
    regular_trading.on_new_entry(new_entry)

    events = regular_trading.on_new_entry(cancel_entry)

    cancel_events = tuple(event for event in events if event.event_type.value == "ORDER_CANCELED")

    assert len(cancel_events) == 1, "Cancel event was not generated"

    assert len(orders_storage.get_all_orders) == 0, "Orders were not removed from the storage"
