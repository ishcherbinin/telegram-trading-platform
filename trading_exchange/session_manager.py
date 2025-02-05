from typing import Any

from trading_exchange.event import Event
from trading_exchange.session_information import SessionInfo
from trading_exchange.sessions.abstract_session import AbstractSession


class SessionManager:

    """
    Class which defines session management mechanism.
    It also stores session statues for each instrument
    """


    def __init__(self, sessions: dict[str, AbstractSession]):
        self._sessions = sessions
        self._session_info: dict[str, SessionInfo] = {}


    def __repr__(self):
        return f"SessionManager(sessions={self._sessions})"


    def get_session_info(self, symbol: str) -> SessionInfo:
        """
        Method to get session info for the symbol
        :param symbol:
        :return:
        """
        session_info = self._session_info.get(symbol)
        if not session_info:
            session_info = SessionInfo(symbol=symbol, current_session="REGULAR", previous_session="REGULAR")
            self._session_info[symbol] = session_info
        return session_info

    def change_session(self, change_session_request: dict[str, Any]) -> list[Event]:
        """
        Method to change session for the symbol
        :param change_session_request:
        :return:
        """
        events = []
        affected_symbols = self._get_affected_symbols(change_session_request)
        for symbol in affected_symbols:
            session_info = self.get_session_info(symbol)
            events.extend(self._end_previous_session(session_info, change_session_request))
            new_session = change_session_request["session"]
            self._update_session_info(session_info, new_session)
            events.extend(self._start_new_session(session_info, change_session_request))

        return events

    def get_current_session_logic(self, symbol: str) -> AbstractSession:
        """
        Method to get current session logic for the symbol
        :param symbol:
        :return:
        """
        session_info = self.get_session_info(symbol)
        return self._sessions[session_info.current_session]

    @staticmethod
    def _update_session_info(session_info: SessionInfo, new_session: str) -> None:
        session_info.previous_session = session_info.current_session
        session_info.current_session = new_session

    def _end_previous_session(self,
                              session_info: SessionInfo,
                              change_session_request: dict[str, Any]) -> list[Event]:
        events = []

        session_logic = self._sessions[session_info.current_session]
        events.extend(session_logic.on_session_end(change_session_request))

        return events

    def _start_new_session(self,
                           session_info: SessionInfo,
                           change_session_request: dict[str, Any]) -> list[Event]:
        session_logic = self._sessions[session_info.current_session]
        return session_logic.on_session_start(change_session_request)

    # noinspection PyMethodMayBeStatic
    def _get_affected_symbols(self, change_session_request: dict[str, Any]) -> list[str]:
        """
        Method to get affected symbols
        :param change_session_request:
        :return:
        """
        return [change_session_request["symbol"]]