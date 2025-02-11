import logging

from event_listeners.abstract_listener import AbstractEventListener
from trading_exchange.event import Event

_logger = logging.getLogger(__name__)

class ListenersManager:

    """
    Class get s list of available listeners and orchestrate their work
    """

    def __init__(self, listeners: list[AbstractEventListener]):
        self._listeners = listeners

    def __repr__(self):
        return f"{self.__class__.__name__} with listeners: {self._listeners}"


    async def process_events(self, events: list[Event]):
        """
        Method processes events by all listeners
        :param events: list of events
        :return:
        """
        for event in events:
            _logger.debug(f"Process event: {event}")
            for listener in self._listeners:
                await listener.listen(event)