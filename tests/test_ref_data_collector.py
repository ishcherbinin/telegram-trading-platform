from decimal import Decimal

from trading_exchange.reference_data import ReferenceData


def test_data_collection(reference_data_class: ReferenceData):
    reference_data_class.set_available_symbols(["RUB/USD", "GEL/USD"])
    reference_data_class.load_data_api_currency()

    reference_data_class.get_reference_price("RUB/USD")

    for symbol in reference_data_class.all_available_symbols:
        assert reference_data_class.get_reference_price(symbol) != Decimal("0"), f"Reference price for {symbol} is not collected"
