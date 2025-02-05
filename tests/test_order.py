from typing import Any

from trading_exchange.order import Order


def test_order_creation_dict(order_data: dict[str, Any]):

    order = Order.from_dict(order_data)

    assert order.id == order_data["id"], "Order id is not equal to the expected value"
    assert order.username == order_data["username"], "Order username is not equal to the expected value"
    assert order.order_qty == order_data["order_qty"], "Order order_qty is not equal to the expected value"
    assert order.order_price == order_data["order_price"], "Order order_price is not equal to the expected value"
    assert order.side.value == order_data["side"].upper(), "Order side is not equal to the expected value"
    assert order.symbol == order_data["symbol"], "Order symbol is not equal to the expected value"
    assert order.time_priority == order_data["time_priority"], "Order time_priority is not equal to the expected value"
    assert order.status.value == "NEW", "Order status is not equal to the expected value"

