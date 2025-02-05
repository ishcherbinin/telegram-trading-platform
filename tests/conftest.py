import logging.config
from typing import Any

import pytest

from logging_conf import log_config
from trading_exchange.entry_processor import EntryProcessor
from trading_exchange.event import Event
from trading_exchange.orders_storage import OrdersStorage
from trading_exchange.session_manager import SessionManager
from trading_exchange.sessions.regular_trading import RegularTrading

logging.config.dictConfig(log_config)

class AuctionSession(RegularTrading):

    def on_new_entry(self, entry: dict[str, Any]) -> list[Event]:
        return []


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

@pytest.fixture(scope="session")
def new_entry() -> dict[str, Any]:
    return {
        "id": "123",
        "username": "test_user",
        "order_qty": 10,
        "order_price": 100,
        "side": "BUY",
        "symbol": "BTC",
        "action": "NEW"
    }

@pytest.fixture
def cancel_entry() -> dict[str, Any]:
    return {
        "id": "123",
        "action": "CANCEL",
        "username": "test_user",
    }

@pytest.fixture
def session_change_request() -> dict[str, Any]:
    return {
        "symbol": "BTC",
        "action": "CHANGE_SESSION",
        "session": "OPEN_AUCTION"
    }

@pytest.fixture(scope="function")
def orders_storage() -> OrdersStorage:
    return OrdersStorage()


@pytest.fixture(scope="function")
def regular_trading(orders_storage: OrdersStorage) -> RegularTrading:
    return RegularTrading(orders_storage)

@pytest.fixture(scope="function")
def session_manager(regular_trading: RegularTrading,
                     orders_storage: OrdersStorage) -> SessionManager:
    return SessionManager(sessions={
        "REGULAR": regular_trading,
        "OPEN_AUCTION": AuctionSession(orders_storage)})

@pytest.fixture(scope="function")
def entry_processor(session_manager: SessionManager) -> EntryProcessor:
    return EntryProcessor(session_manager)