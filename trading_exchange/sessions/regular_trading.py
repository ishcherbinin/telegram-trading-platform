import logging
from decimal import Decimal
from typing import Any

from trading_exchange.enums import EventTypeEnum, SideEnum, OrderStatusEnum
from trading_exchange.event import Event
from trading_exchange.order import Order
from trading_exchange.sessions.abstract_session import AbstractSession
from trading_exchange.trade import Trade

_logger = logging.getLogger(__name__)


class RegularTrading(AbstractSession):

    def on_new_entry(self, entry: dict[str, Any]) -> list[Event]:
        _logger.debug(f"New entry received: {entry}")
        if entry["action"] == "NEW":
            return self._on_new_order(entry)
        if entry["action"] == "CANCEL":
            return self._on_cancel_order(entry)
        _logger.debug("Incorrect action for regular trading")
        return []


    def _on_new_order(self, entry: dict[str, Any]) -> list[Event]:
        _logger.debug("Process new order entity")

        events: list[Event] = []

        order = self._build_order(entry)
        events.extend(self._check_for_trade(order))
        events.extend(self._add_new_order(order))

        self._orders_storage.clear_terminated_orders()
        return events

    def _normalize_entry(self, entry: dict[str, Any]) -> dict[str, Any]:
        entry["time_priority"] = self._orders_storage.get_order_time_priority
        _logger.debug(f"Normalized entry: {entry}")
        return entry

    def _build_order(self, entry: dict[str, Any]) -> Order:
        entry = self._normalize_entry(entry)
        order = Order.from_dict(entry)
        return order

    def _check_for_trade(self, order: Order) -> list[Event]:
        _logger.debug(f"Check for trade for order: {order}")
        events: list[Event] = []
        contra_orders = self._select_contra_orders(order)
        self._sort_orders_for_trade(order, contra_orders)
        tradable_orders = self._get_tradable_orders(order, contra_orders)
        for passive_order in tradable_orders:
            events.extend(self._trade_two_orders(order, passive_order))
        return events

    def _select_contra_orders(self, aggr_order: Order) -> list[Order]:
        all_orders = self._orders_storage.get_all_orders
        return [order for order in all_orders if self._is_contra_order(aggr_order, order)]

    @staticmethod
    def _is_contra_order(aggr_order: Order, order: Order) -> bool:
        contra_side = SideEnum.SELL if aggr_order.side == SideEnum.BUY else SideEnum.BUY
        return (order.side == contra_side and order.symbol == aggr_order.symbol
                and order.username != aggr_order.username)

    def _add_new_order(self, order: Order) -> list[Event]:
        if order.leaves_qty > 0:
            self._orders_storage.add_order(order)
            return [Event(EventTypeEnum.ORDER_ADDED, order)]
        return []

    @staticmethod
    def _sort_orders_for_trade(aggr_order: Order, contra_orders: list[Order]) -> None:
        """
        Standard sorting for regular trading. On most exchanges it is price time priority
        :param aggr_order:
        :param contra_orders:
        :return:
        """

        _logger.debug(f"Sort orders for trade: {aggr_order} and {contra_orders}")

        contra_orders.sort(key=lambda order: order.time_priority)

        contra_orders.sort(key=lambda order: order.order_price)

    @staticmethod
    def _get_tradable_orders(aggr_order: Order, contra_orders: list[Order]) -> tuple[Order, ...]:
        """
        Method selects orders which are suitable for trade.
        Implementation depends on the exchange rules. Default is price comparison

        For buy order it will be orders with price less or equal to the price of aggr_order
        For sale order it will be orders with price greater or equal to the price of aggr_order

        :param aggr_order:
        :param contra_orders:
        :return:
        """

        if aggr_order.side == SideEnum.BUY:
            return tuple(order for order in contra_orders if order.trade_price <= aggr_order.trade_price)
        return tuple(order for order in contra_orders if order.trade_price >= aggr_order.trade_price)

    @staticmethod
    def _update_order(order: Order, trd_price: Decimal, trd_qty: Decimal) -> None:
        order.last_price = trd_price
        order.last_qty = trd_qty
        order.leaves_qty -= trd_qty
        order.cum_qty += trd_qty
        if order.leaves_qty == 0:
            order.status = OrderStatusEnum.FILLED
        else:
            order.status = OrderStatusEnum.PARTIALLY_FILLED

    def _trade_two_orders(self, aggr_order: Order, passive_order: Order) -> list[Event]:
        events = []
        trd_price = self._calculate_trade_price(aggr_order, passive_order)
        trd_qty = min(aggr_order.leaves_qty, passive_order.leaves_qty)
        _logger.debug(f"Trade qty {trd_qty} of {aggr_order} and {passive_order} at price {trd_price}")
        for order in (aggr_order, passive_order):
            self._update_order(order, trd_price, trd_qty)
        trade_entity =  self._build_trade_entity(
            symbol=aggr_order.symbol,
            trade_price=trd_price,
            trade_qty=trd_qty,
            passive_user=passive_order.username,
            aggressive_user=aggr_order.username
        )
        events.append(Event(EventTypeEnum.ORDER_TRADED, trade_entity))
        self._trade_storage.add_trade_to_storage(trade_entity)
        return events

    def _build_trade_entity(self, symbol: str,
                            trade_price: Decimal,
                            trade_qty: Decimal,
                            passive_user: str,
                            aggressive_user: str) -> Trade:
        """
        Method builds trade entity
        :param symbol:
        :param trade_price:
        :param trade_qty:
        :param passive_user:
        :param aggressive_user:
        :return:
        """

        return Trade(
            trade_id=self._trade_storage.get_trade_id_counter(),
            symbol=symbol,
            trade_price=trade_price,
            trade_qty=trade_qty,
            passive_username=passive_user,
            aggressive_username=aggressive_user
        )


    # noinspection PyMethodMayBeStatic
    # noinspection PyUnusedLocal
    def _calculate_trade_price(self, aggr_order: Order, passive_order: Order) -> Decimal:
        return passive_order.trade_price

    def _on_cancel_order(self, entry: dict[str, Any]) -> list[Event]:
        _logger.debug("Process cancel order entity")
        order_id = entry["id"]
        order = self._orders_storage.get_order_by_id(order_id)
        if order is None:
            _logger.debug(f"Order with id {order_id} not found")
            return []
        self._orders_storage.remove_order_by_id(order_id)
        return [Event(EventTypeEnum.ORDER_CANCELED, order)]