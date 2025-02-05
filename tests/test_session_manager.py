from trading_exchange.session_information import SessionInfo
from trading_exchange.session_manager import SessionManager


def test_get_session_info(session_manager: SessionManager):
    session_info: SessionInfo = session_manager.get_session_info("BTC")
    assert session_info.symbol == "BTC", "Symbol is not equal"
    assert session_info.current_session == "REGULAR", "Current session is not equal"
    assert session_info.previous_session == "REGULAR", "Previous session is not equal"

def test_session_change(
        session_manager: SessionManager,
        session_change_request: dict[str, str],
):
    session_manager.change_session(session_change_request)

    session_info: SessionInfo = session_manager.get_session_info("BTC")

    assert session_info.symbol == "BTC", "Symbol is not equal"

    assert session_info.current_session == "OPEN_AUCTION", "Current session is not equal"

    assert session_info.previous_session == "REGULAR", "Previous session is not equal"