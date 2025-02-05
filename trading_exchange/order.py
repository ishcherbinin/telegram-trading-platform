from dataclasses import dataclass
from decimal import Decimal
from typing import Any

from trading_exchange.enums import SideEnum, OrderStatusEnum


@dataclass(repr=True)
class Order:

    """
    Class represents order with defined fields and actions available for it.
    """

    id: str
    username: str
    order_qty: Decimal
    order_price: Decimal
    side: SideEnum
    symbol: str
    status: OrderStatusEnum
    time_priority: int
    last_price: Decimal = Decimal(0)
    last_qty: Decimal = Decimal(0)
    leaves_qty: Decimal = Decimal(0)
    cum_qty: Decimal = Decimal(0)


    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> "Order":
        return cls(
            id=data["id"],
            username=data["username"],
            order_qty=Decimal(data["order_qty"]),
            order_price=Decimal(data["order_price"]),
            side=SideEnum(data["side"].upper()),
            symbol=data["symbol"],
            status=OrderStatusEnum.NEW,
            time_priority=data["time_priority"],
            leaves_qty=Decimal(data["order_qty"]),
        )

    def to_dict(self) -> dict[str, Any]:
        dict_ = self.__dict__.copy()
        dict_["side"] = self.side.value
        dict_["status"] = self.status.value
        return dict_

    @property
    def trade_price(self) -> Decimal:
        return self.order_price