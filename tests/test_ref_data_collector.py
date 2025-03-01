from decimal import Decimal
from pathlib import Path

from trading_exchange.reference_data import ReferenceData


def test_data_collection(reference_data_class: ReferenceData, reference_data_tables_path: Path):
    reference_data_class.load_ref_data_tables(reference_data_tables_path)

    reference_data_class.load_data_api_currency()

    for symbol in reference_data_class.all_available_symbols:
        assert reference_data_class.get_reference_price(symbol) != Decimal("0"), f"Reference price for {symbol} is not collected"
