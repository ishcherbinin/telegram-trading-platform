from dataclasses import dataclass
from decimal import Decimal
from typing import Any


@dataclass(repr=True)
class Trade:
    trade_id: int
    symbol: str
    trade_price: Decimal
    trade_qty: Decimal
    passive_username: str
    aggressive_username: str

    def to_dict(self) -> dict[str, Any]:
        return {
            "trade_id": self.trade_id,
            "symbol": self.symbol,
            "trade_price": self.trade_price,
            "trade_qty": self.trade_qty,
            "passive_username": self.passive_username,
            "aggressive_username": self.aggressive_username
        }