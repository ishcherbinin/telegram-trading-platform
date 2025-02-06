from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from telegram_int_utils.fsm_states import RequestStates
from telegram_int_utils.text_storage import BaseTextStorage
from telegram_int_utils.utils import validate_chat_id, print_order
from trading_exchange.entry_processor import EntryProcessor
from trading_exchange.exchange_builder import ExchangeBuilder
from trading_exchange.orders_storage import OrdersStorage
from trading_exchange.session_manager import SessionManager


class MessageHandler:

    """
    Class which handles messages and states of telegram bot
    It takes as a parameters bot itself, dispatcher text storage and exchange processor

    """

    def __init__(self,
                 bot: Bot,
                 dispatcher: Dispatcher,
                 allowed_ids: list[str],
                 text_storage: BaseTextStorage,
                 exchange_builder: ExchangeBuilder):
        self._bot = bot
        self._dispatcher = dispatcher
        self._text_storage = text_storage
        self._entry_processor: EntryProcessor = exchange_builder.entry_processor
        self._orders_storage: OrdersStorage = exchange_builder.orders_storage
        self._session_manager: SessionManager = exchange_builder.session_manager
        self._chat_id_per_user = {}
        self._allowed_ids = allowed_ids

    def __repr__(self):
        return (f"{self.__class__.__name__}({self._bot}, {self._dispatcher}, "
                f"{self._text_storage}, {self._entry_processor})")

    def register_handlers(self):
        self._dispatcher.message.register(self._start_command, Command("start", "help"))
        self._dispatcher.message.register(self._get_id_command, Command("getid"))
        self._dispatcher.message.register(self._my_orders_command, Command("myorders"))
        self._dispatcher.message.register(self._all_orders_command, Command("showallorders"))

    async def _start_command(self, message: types.Message):
        id_ = str(message.chat.id)
        msg = (self._text_storage.HELP_CLIENT
               if await validate_chat_id(id_, self._allowed_ids)
               else self._text_storage.HELP_MANAGERS)
        await message.answer(msg)

    async def _get_id_command(self, message: types.Message):
        id_ = str(message.chat.id)
        await message.answer(f"{self._text_storage.CHAT_ID_MESSAGE} {id_}")

    async def _my_orders_command(self, message: types.Message):
        all_user_orders = self._orders_storage.get_orders_by_username(str(message.chat.username))
        if len(all_user_orders) == 0:
            await message.answer(self._text_storage.NO_ACTIVE_ORDER_MESSAGE)
        for order in all_user_orders:
            await print_order(message, order)

    async def _all_orders_command(self, message: types.Message, state: FSMContext):
        if await validate_chat_id(str(message.chat.id), self._allowed_ids):
            await message.answer(self._text_storage.TEXT_NO_PERMISSIONS_FOR_COMMAND)
            await state.clear()
        all_orders = self._orders_storage.get_all_orders
        if len(all_orders) == 0:
            await message.answer(self._text_storage.NO_ACTIVE_ORDER_MESSAGE)
        for order in all_orders:
            await print_order(message, order)

    # noinspection PyMethodMayBeStatic
    async def _get_current_session_command(self, message: types.Message, state: FSMContext):
        await message.answer(self._text_storage.REQUEST_FOR_SYMBOL_FOR_SESSION_CHECK)
        await state.set_state(RequestStates.wait_for_symbol_for_session_state)

    async def _get_current_session(self, message: types.Message, state: FSMContext):
        symbol = message.text
        session = self._session_manager.get_session_info(symbol).current_session
        await message.answer(f"{self._text_storage.TEXT_CURRENT_SESSION_ON_INSTRUMENT} {session}")
        await state.clear()

