from typing import Any

import pytest

from trading_exchange.orders_storage import OrdersStorage


@pytest.fixture(scope="session")
def order_data() -> dict[str, Any]:
    return {
        "id": "123",
        "username": "test_user",
        "order_qty": 10,
        "order_price": 100,
        "side": "BUY",
        "symbol": "BTC",
        "time_priority": 0,
    }

@pytest.fixture(scope="function")
def orders_storage() -> OrdersStorage:
    return OrdersStorage()
