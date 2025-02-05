from dataclasses import dataclass


@dataclass(repr=True)
class SessionInfo:

    """
    Class to store session information for a given symbol (current session on instrument)
    """

    symbol: str
    current_session: str
    previous_session: str
