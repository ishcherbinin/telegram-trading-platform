import logging
from abc import ABC, abstractmethod
from typing import Any

_logger = logging.getLogger(__name__)

class AbstractDataConverter(ABC):

    """
    Class defines converter from entry data format to format used in entry processor class
    """

    def __repr__(self):
        return f"{self.__class__.__name__}"

    @abstractmethod
    def convert(self, data: dict[str, Any]) -> Any:
        pass

class TgDataConverter(AbstractDataConverter):

    """
    Class defines converter for telegram data

    """

    def convert(self, data: dict[str, Any]) -> Any:
        _logger.debug(f"Converting data: {data}")
        return {
            "id": data["id"],
            "username": data["username"],
            "action": data["action"],
            "symbol": data["symbol"],
            "order_price": data["price"],
            "order_qty": data["quantity"],
            "side": data["side"].upper(),
        }

