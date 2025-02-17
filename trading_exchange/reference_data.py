import logging
from decimal import Decimal
from typing import Any
import requests
from urllib.parse import urlparse, urljoin

_logger = logging.getLogger(__name__)

class ReferenceData:

    """
    Class defines methods and storage for reference data per symbol/instrument

    It might be overridden with another implementation if required but should have same tables and it's fields
    """


    def __init__(self):
        self._instrument_data: dict[str, dict[str, Any]] = {}
        self._api_end_point = urlparse("https://open.er-api.com/v6/latest/")

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def load_data_api_currency(self):
        for instrument in self.available_symbols():
            target_instrument, source_instrument = instrument.split("/")
            api_data = self._get_data_from_api(target_instrument)
            if not api_data:
                continue
            rates = api_data.get("rates", {})
            ref_price = self._get_ref_price_for_currency(rates, source_instrument)
            self._instrument_data[instrument] = {"reference_price": ref_price}

    # noinspection PyMethodMayBeStatic
    def _get_ref_price_for_currency(self, rates: dict[str, float],
                                    source_instrument: str) -> Decimal:
        rate = rates.get(source_instrument, 0.0)
        ref_price = Decimal(str(rate))
        return ref_price

    def _get_data_from_api(self, target_instrument: str) -> dict[str, Any]:
        # Here should be implementation to get data from API
        response = requests.get(urljoin(self._api_end_point.geturl(), target_instrument))
        if response.status_code != 200:
            _logger.error(f"Failed to get data from API for instrument {target_instrument}, "
                          f"status code: {response.status_code}")
            return {}
        return response.json()

    def get_reference_price(self, symbol: str) -> Decimal:
        return self._instrument_data.get(symbol, {}).get("reference_price", Decimal(0.0))

    # noinspection PyMethodMayBeStatic
    def available_symbols(self) -> list[str]:
        return ["RUB/USD", "GEL/USD"]