import logging
from typing import List, Any

from trading_exchange.validations.abstract_validator import AbstractValidator

_logger = logging.getLogger(__name__)

class ValidationManager:

    """
    Class for managing all validators
    """

    def __init__(self, validators: List[AbstractValidator]):
        self._validators = validators

    def validate(self, data: dict[str, Any]):
        """
        Method validates data using all validators
        :param data:
        :return:
        """
        _logger.debug(f"Validating data: {data}")
        for validator in self._validators:
            _logger.debug(f"Using validator: {validator}")
            if not validator.validate(data):
                break