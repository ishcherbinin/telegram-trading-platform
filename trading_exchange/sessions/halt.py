from typing import Any

from trading_exchange.event import Event
from trading_exchange.sessions.abstract_session import AbstractSession


class Halt(AbstractSession):

    def on_new_entry(self, entry: dict[str, Any]) -> list[Event]:
        return []