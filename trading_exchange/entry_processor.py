import logging
from typing import Any

from trading_exchange.enums import EventTypeEnum
from trading_exchange.event import Event
from trading_exchange.session_manager import SessionManager
from trading_exchange.sessions.abstract_session import AbstractSession
from trading_exchange.validations.validation_manager import ValidationManager

_logger = logging.getLogger(__name__)

class EntryProcessor:

    """
    Class orchestrate whole execution, It gets entry and work with it
    """

    def __init__(self,
                 session_manager: SessionManager,
                 validation_manager: ValidationManager):
        self._session_manager = session_manager
        self._validation_manager = validation_manager
        self._events: list[Event] = []

    def process_entry(self, entry: dict[str, Any]) -> list[Event]:
        _logger.debug(f"Processing entry: {entry}")
        if entry["action"] == "CHANGE_SESSION":
            events = self._session_manager.change_session(entry)
        else:
            events = self._process_business_entry(entry)

        self._events.extend(events)
        return events

    def _process_business_entry(self, entry: dict[str, Any]) -> list[Event]:
        """
        method process events related to business logic of matching engine such as new order, cancel order, etc.
        :param entry:
        :return:
        """
        events: list[Event] = []
        self._validation_manager.validate(entry)
        if entry.get("ValidationErrors"):
            _logger.debug(f"Validation errors: {entry['ValidationErrors']}")
            events.append(Event(EventTypeEnum.ORDER_REJECTED, info=entry))
            return events

        current_session_logic: AbstractSession = self._session_manager.get_current_session_logic(entry["symbol"])
        events = current_session_logic.on_new_entry(entry)
        return events
