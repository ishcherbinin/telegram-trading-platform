from dataclasses import dataclass


@dataclass(repr=True)
class SessionInfo:
    symbol: str
    current_session: str
    previous_session: str
