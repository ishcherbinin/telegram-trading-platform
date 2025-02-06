import logging
from dataclasses import dataclass

from trading_exchange.entry_processor import EntryProcessor
from trading_exchange.orders_storage import OrdersStorage
from trading_exchange.session_manager import SessionManager
from trading_exchange.sessions.abstract_session import AbstractSession
from trading_exchange.sessions.regular_trading import RegularTrading

_logger = logging.getLogger(__name__)


@dataclass(repr=True)
class ExchangeBuilder:
    """
    Class builds trading exchange instance with defined fields and actions available for it.
    """

    def __init__(self):
        self.entry_processor = None
        self.orders_storage = None
        self.session_manager = None

    def build_exchange(self):

        _logger.debug("Building exchange")

        self.orders_storage = self._build_orders_storage()
        sessions = self._build_sessions(self.orders_storage)
        self.session_manager = self._build_session_manager(sessions)
        self.entry_processor = EntryProcessor(self.session_manager)

    # noinspection PyMethodMayBeStatic
    def _build_session_manager(self, sessions: dict[str, AbstractSession]) -> SessionManager:
        return SessionManager(sessions)

    # noinspection PyMethodMayBeStatic
    def _build_orders_storage(self) -> OrdersStorage:
        return OrdersStorage()

    # noinspection PyMethodMayBeStatic
    def _build_sessions(self, order_storage: OrdersStorage) -> dict[str, AbstractSession]:
        return {
            "REGULAR": RegularTrading(order_storage),
        }
