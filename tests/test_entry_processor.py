from typing import Any

from trading_exchange.entry_processor import EntryProcessor
from trading_exchange.orders_storage import OrdersStorage


def test_new_entry_handling(
        entry_processor: EntryProcessor,
        orders_storage: OrdersStorage,
        new_entry: dict[str, Any],
    ):
    events = entry_processor.process_entry(new_entry)
    assert len(events) > 0, "No events were generated"

    new_events  = tuple(filter(lambda event: event.event_type.value == "ORDER_ADDED", events))

    assert len(new_events) == 1, "No ORDER_ADDED event was generated"

    order = orders_storage.get_order_by_id(new_entry["id"])

    assert order is not None, "Order was not added to the storage"



