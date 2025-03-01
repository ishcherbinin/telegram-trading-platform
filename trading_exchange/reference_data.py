import csv
import logging
from decimal import Decimal
from pathlib import Path
from typing import Any, Union
from urllib.parse import urlparse, urljoin

import requests

_logger = logging.getLogger(__name__)


class ReferenceData:
    """
    Class defines methods and storage for reference data per symbol/instrument

    It might be overridden with another implementation if required but should have same tables and it's fields
    """

    def __init__(self):
        self._instrument_data: dict[str, dict[str, Any]] = {}
        self._api_end_point = urlparse("https://open.er-api.com/v6/latest/")
        self._available_symbols: list[str] = []

    def __repr__(self):
        return f"{self.__class__.__name__}"

    def load_ref_data_tables(self, tables_path: Union[str, Path]):
        """
        Load reference data tables from files located near model
        :return:
        """
        if not tables_path.exists():
            _logger.error(f"Tables path {tables_path} does not exist")
            return
        _logger.debug(f"Loading reference data tables from {tables_path}")
        instrument_file = tables_path / "instruments.csv"
        with open(instrument_file, "r") as f:
            reader = csv.DictReader(f)
            for row in reader:
                symbol = row["symbol"]
                if symbol in self._available_symbols:
                    _logger.debug(f"Load symbol: {symbol} params: {row}")
                    self._instrument_data[symbol] = row


    def load_data_api_currency(self):
        for instrument in self._available_symbols:
            target_instrument, source_instrument = instrument.split("/")
            api_data = self._get_data_from_api(target_instrument)
            if not api_data:
                continue
            rates = api_data.get("rates", {})
            ref_price = self._get_ref_price_for_currency(rates, source_instrument)
            _logger.debug(f"Currency pair: {instrument}, reference price: {ref_price}")
            self._instrument_data[instrument].update({"reference_price": ref_price})

    # noinspection PyMethodMayBeStatic
    def _get_ref_price_for_currency(self, rates: dict[str, float],
                                    source_instrument: str) -> Decimal:
        rate = rates.get(source_instrument, 0.0)
        ref_price = Decimal(str(rate)).quantize(Decimal("0.0001"))
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

    def get_price_band_percentage(self, symbol: str) -> Decimal:
        return Decimal(self._instrument_data.get(symbol, {}).get("price_band_percentages", Decimal(0.0)))

    # noinspection PyMethodMayBeStatic
    def set_available_symbols(self, symbols: list[str]):
        self._available_symbols = symbols

    @property
    def all_available_symbols(self):
        return self._available_symbols
