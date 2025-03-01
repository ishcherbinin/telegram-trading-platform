import logging
from decimal import Decimal

from trading_exchange.reference_data import ReferenceData
from trading_exchange.validations.abstract_validator import AbstractValidator

_logger = logging.getLogger(__name__)

class PriceBandValidator(AbstractValidator):

    """
    PriceBandValidator class to validate price of the order on entry and reject if it exceeds some range
    """

    def __init__(self, ref_data: ReferenceData):
        self._ref_data = ref_data

    def validate(self, data: dict) -> bool:
        """
        Method validates price of the order, if it exceeds some range it will be rejected
        :param data:
        :return:
        """
        symbol = data["symbol"]
        price = Decimal(data["order_price"])
        price_band = self._ref_data.get_price_band_percentage(symbol)
        if price_band == 0:
            _logger.debug(f"Price band for symbol {symbol} is not set")
            return True
        ref_price = self._ref_data.get_reference_price(symbol)
        if ref_price == 0:
            _logger.debug(f"Reference price for symbol {symbol} is not set")
            return True
        upper_limit = (ref_price + (ref_price * price_band / Decimal(100)))
        lower_limit = (ref_price - (ref_price * price_band / Decimal(100)))
        if price < lower_limit or price > upper_limit:
            _logger.debug(f"Price is out of price band for symbol {symbol}")
            data["ValidationErrors"] = (f"Price is out of price band. "
                                        f"Lower limit: {lower_limit}, Upper limit: {upper_limit}")
            return False
        return True