from typing import Any

from aiogram import Bot

from event_listeners.abstract_listener import AbstractEventListener
from telegram_interface.ids_storage import TgIdsStorage
from telegram_interface.text_storage import BaseTextStorage
from trading_exchange.event import Event
from trading_exchange.trade import Trade


class TgEventListener(AbstractEventListener):

    """
    Class defines processing of events for Telegram bot
    """

    def __init__(self,
                 bot: Bot,
                 tg_ids_storage: TgIdsStorage,
                 text_storage: BaseTextStorage):
        self._bot = bot
        self._tg_ids_storage = tg_ids_storage
        self._text_storage = text_storage

    async def listen(self, event: Event):
        event_name: str = event.event_type.value
        if event_name == "ORDER_TRADED":
            trade: Trade = event.info
            await self._process_trade_event_managers(trade)
            await self._notify_users_about_trade(trade)
        if event_name == "ORDER_REJECTED":
            await self._notify_users_about_rejected_order(event.info)

    async def _process_trade_event_managers(self, trade: Trade):
        """
        Method processes trade event (send notification to managers)
        :param trade:
        :return:
        """
        _managers_ids = self._tg_ids_storage.get_managers_ids()
        for chat_id in _managers_ids:
            msg = self._text_storage.MANAGERS_NOTIFICATION_ABOUT_TRADE.format(**trade.to_dict())
            await self._bot.send_message(chat_id, msg)

    async def _notify_users_about_trade(self, trade: Trade):
        """
        Method notifies users about trade event
        :param trade:
        :return:
        """
        users = (trade.aggressive_username, trade.passive_username)
        for user in users:
            chat_id = self._tg_ids_storage.get_user_ids(user)
            if chat_id:
                msg = self._text_storage.USER_TRADE_NOTIFICATION.format(**{"trade_price": trade.trade_price,
                                                                         "trade_qty": trade.trade_qty})
                await self._bot.send_message(chat_id, msg)

    async def _notify_users_about_rejected_order(self, info: dict[str, Any]):
        """
        Notify user about order being rejected
        :param info:
        :return:
        """
        chat_id = self._tg_ids_storage.get_user_ids(info["username"])
        if chat_id:
            errors = info.get("ValidationErrors", "Unknown error")
            msg = self._text_storage.ORDER_REJECTION_BY_VALIDATION_TEXT.format(validation_errors=errors)
            await self._bot.send_message(chat_id, msg)
