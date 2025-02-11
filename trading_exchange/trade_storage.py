from typing import Optional

from trading_exchange.trade import Trade


class TradeStorage:


    """
    TradeStorage is a class that stores trades for a given trading pair.
    """

    def __init__(self):
        self._trades: list[Trade] = []
        self._trade_counter: int = 0


    def get_trade_id_counter(self) -> int:
        """
        Method returns trade counter value
        :return: trade counter
        """
        self._trade_counter += 1
        return self._trade_counter


    def add_trade_to_storage(self, trade: Trade) -> None:
        """
        Method adds trade to storage
        :param trade: trade to add
        :return:
        """
        self._trades.append(trade)

    def find_trade_by_id(self, trade_id: int) -> Optional[Trade]:
        return next((trade for trade in self._trades if trade.trade_id == trade_id), None)

    def remove_trade_from_storage(self, trade: Trade) -> None:
        """
        Method removes trade from storage
        :param trade: trade to remove
        :return:
        """
        self._trades.remove(trade)

    @property
    def get_all_trades(self) -> list[Trade]:
        """
        Method returns all trades from storage
        :return: list of trades
        """
        return self._trades