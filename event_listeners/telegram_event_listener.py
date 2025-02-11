from event_listeners.abstract_listener import AbstractEventListener
from telegram_interface.text_storage import BaseTextStorage
from trading_exchange.event import Event
from aiogram import Bot

from trading_exchange.trade import Trade


class TgEventListener(AbstractEventListener):

    """
    Class defines processing of events for Telegram bot
    """

    def __init__(self,
                 bot: Bot,
                 managers_ids: list[int],
                 text_storage: BaseTextStorage):
        self._bot = bot
        self._managers_ids = managers_ids
        self._text_storage = text_storage

    async def listen(self, event: Event):
        event_name: str = event.event_type.value
        if event_name == "ORDER_TRADED":
            trade: Trade = event.info
            await self._process_trade_event(trade)


    async def _process_trade_event(self, trade: Trade):
        """
        Method processes trade event (send notification to managers)
        :param trade:
        :return:
        """
        for chat_id in self._managers_ids:
            msg = self._text_storage.MANAGERS_NOTIFICATION_ABOUT_TRADE.format(**trade.to_dict())
            await self._bot.send_message(chat_id, msg)
