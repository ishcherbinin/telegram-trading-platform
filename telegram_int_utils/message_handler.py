from aiogram import Bot, Dispatcher, types

from telegram_int_utils.text_storage import AbstractTextStorage
from telegram_int_utils.utils import validate_chat_id
from trading_exchange.entry_processor import EntryProcessor


class MessageHandler:

    """
    Class which handles messages and states of telegram bot
    It takes as a parameters bot itself, dispatcher text storage and exchange processor

    """

    def __init__(self,
                 bot: Bot,
                 dispatcher: Dispatcher,
                 allowed_ids: list[str],
                 text_storage: AbstractTextStorage,
                 entry_processor: EntryProcessor):
        self._bot = bot
        self._dispatcher = dispatcher
        self._text_storage = text_storage
        self._entry_processor = entry_processor
        self._chat_id_per_user = {}
        self._allowed_ids = allowed_ids

    def __repr__(self):
        return f"{self.__class__.__name__}({self._bot}, {self._dispatcher}, {self._text_storage}, {self._entry_processor})"

    def register_handlers(self):
        self._dispatcher.message.register(self.start_command, commands=["start", "help"], state="*")

    async def start_command(self, message: types.Message):
        await message.answer(self._text_storage.COMMON_GREETING)
        id_ = str(message.chat.id)
        msg = (self._text_storage.HELP_CLIENT
               if validate_chat_id(id_, self._allowed_ids)
               else self._text_storage.HELP_MANAGERS)
        await message.answer(msg)
