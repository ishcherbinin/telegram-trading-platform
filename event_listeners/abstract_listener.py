from abc import ABC, abstractmethod

from trading_exchange.event import Event


class AbstractEventListener(ABC):

    """
    Class defines strategy for creating event listeners of exchange

    """

    def __repr__(self):
        return self.__class__.__name__

    @abstractmethod
    def listen(self, event: Event):
        pass