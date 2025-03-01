from abc import abstractmethod, ABC
from typing import Any


class AbstractValidator(ABC):

    """
    Abstract class for all validators.
    """

    def __repr__(self):
        return f"{self.__class__.__name__}"

    @abstractmethod
    def validate(self, data: dict[str, Any]) -> bool:

        pass