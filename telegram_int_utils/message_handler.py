import logging
from typing import Any

from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from telegram_int_utils.data_converter import AbstractDataConverter
from telegram_int_utils.fsm_states import RequestStates
from telegram_int_utils.text_storage import BaseTextStorage
from telegram_int_utils.utils import validate_chat_id, print_order
from trading_exchange.entry_processor import EntryProcessor
from trading_exchange.exchange_builder import ExchangeBuilder
from trading_exchange.orders_storage import OrdersStorage
from trading_exchange.session_manager import SessionManager

_logger = logging.getLogger(__name__)


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
                 exchange_builder: ExchangeBuilder,
                 data_converter: AbstractDataConverter):
        self._bot = bot
        self._dispatcher = dispatcher
        self._text_storage = text_storage
        self._entry_processor: EntryProcessor = exchange_builder.entry_processor
        self._orders_storage: OrdersStorage = exchange_builder.orders_storage
        self._session_manager: SessionManager = exchange_builder.session_manager
        self._chat_id_per_user = {}
        self._allowed_ids = allowed_ids
        self._data_converter = data_converter

    def __repr__(self):
        return (f"{self.__class__.__name__}({self._bot}, {self._dispatcher}, "
                f"{self._text_storage}, {self._entry_processor})")

    def register_handlers(self):
        self._dispatcher.message.register(self._start_command, Command("start", "help"))
        self._dispatcher.message.register(self._get_id_command, Command("getid"))
        self._dispatcher.message.register(self._my_orders_command, Command("myorders"))
        self._dispatcher.message.register(self._all_orders_command, Command("showallorders"))
        self._dispatcher.message.register(self._exit_command, Command("exit"))
        self._dispatcher.message.register(self._get_current_session_command, Command("currentsession"))
        self._dispatcher.message.register(self._get_current_session, RequestStates.wait_for_symbol_for_session_state)
        self._dispatcher.message.register(self._cancel_order_command, Command("cancelorder"))
        self._dispatcher.message.register(self._process_cancel_order, RequestStates.wait_for_id_for_cancel_state)

        self._dispatcher.message.register(self._new_order_command, Command("neworder"))
        self._dispatcher.callback_query.register(self._process_selection,
                                                 F.data.in_(["select_side", "select_symbol"]))
        self._dispatcher.callback_query.register(self._process_side_or_symbol, F.data.startswith("set_"))
        self._dispatcher.callback_query.register(self._enter_price, F.data == "enter_price")
        self._dispatcher.callback_query.register(self._enter_quantity, F.data == "enter_quantity")
        self._dispatcher.message.register(self._process_price, RequestStates.wait_for_order_price)
        self._dispatcher.message.register(self._process_quantity, RequestStates.wait_for_order_quantity)
        self._dispatcher.callback_query.register(self._confirm_order, F.data == "confirm_order")

    async def _start_command(self, message: types.Message):
        id_ = str(message.chat.id)
        msg = (self._text_storage.HELP_CLIENT
               if await validate_chat_id(id_, self._allowed_ids)
               else self._text_storage.HELP_MANAGERS)
        await message.answer(msg)

    async def _get_id_command(self, message: types.Message):
        id_ = str(message.chat.id)
        await message.answer(f"{self._text_storage.CHAT_ID_MESSAGE} {id_}")

    async def _exit_command(self, message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer(self._text_storage.TEXT_EXIT_MESSAGE)

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

    async def _new_order_command(self, message: types.Message, state: FSMContext):
        await state.update_data(side=None, symbol=None, price=None, quantity=None, action="NEW")
        await message.answer(self._text_storage.REQUEST_FOR_ORDER_DETAILS_MESSAGE,
                             reply_markup=self._get_order_keyboard({}))

    # noinspection PyUnusedLocal
    async def _process_selection(self, callback: types.CallbackQuery, state: FSMContext):
        """Handle side & symbol selection."""
        if callback.data == "select_side":
            _logger.debug("Select side")
            buttons = self._side_buttons
            await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

        elif callback.data == "select_symbol":
            _logger.debug("Select symbol")
            buttons = self._symbol_buttons
            await callback.message.edit_reply_markup(reply_markup=InlineKeyboardMarkup(inline_keyboard=buttons))

    async def _process_side_or_symbol(self, callback: types.CallbackQuery, state: FSMContext):
        """Save side or symbol and update order form."""
        key, value = callback.data.split(":")
        _logger.debug(f"Key: {key}, value: {value}")
        await state.update_data({key.replace("set_", ""): value})
        data = await state.get_data()
        await callback.message.edit_text(self._text_storage.FILL_ORDER_DETAILS_REQUEST_MESSAGE,
                                         reply_markup=self._get_order_keyboard(data))

    async def _enter_price(self, callback: types.CallbackQuery, state: FSMContext):
        """Ask user to enter price manually."""
        await callback.message.answer(self._text_storage.REQUEST_FOR_ORDER_PRICE_MESSAGE)
        await state.set_state(RequestStates.wait_for_order_price)

    async def _enter_quantity(self, callback: types.CallbackQuery, state: FSMContext):
        """Ask user to enter quantity manually."""
        await callback.message.answer(self._text_storage.REQUEST_FOR_ORDER_QUANTITY_MESSAGE)
        await state.set_state(RequestStates.wait_for_order_quantity)

    async def _process_price(self, message: types.Message, state: FSMContext):
        """Save price and update order form."""
        _logger.debug(f"Price: {message.text}")
        await state.update_data(price=message.text)
        data = await state.get_data()
        await message.answer(self._text_storage.FILL_ORDER_DETAILS_REQUEST_MESSAGE,
                             reply_markup=self._get_order_keyboard(data))

    async def _process_quantity(self, message: types.Message, state: FSMContext):
        """Save quantity and update order form."""
        _logger.debug(f"Quantity: {message.text}")
        await state.update_data(quantity=message.text)
        data = await state.get_data()
        await message.answer(self._text_storage.FILL_ORDER_DETAILS_REQUEST_MESSAGE,
                             reply_markup=self._get_order_keyboard(data))

    async def _confirm_order(self, callback: types.CallbackQuery, state: FSMContext):
        """Create order and send it to exchange."""
        data = await state.get_data()
        if None in data.values():
            await callback.answer(self._text_storage.WARNING_FOR_EMPTY_FIELDS)
            return
        assigned_data = self._assign_service_fields(message=callback.message, data=data)
        _logger.debug(f"Assigned data: {assigned_data}")
        order_data = self._data_converter.convert(assigned_data)
        _logger.debug(f"Order data: {order_data}")
        _ = self._entry_processor.process_entry(order_data)
        await callback.message.answer(self._text_storage.CONFIRMATION_OF_ORDER_CREATION_MESSAGE)
        await state.clear()
        self._chat_id_per_user[order_data["username"]] = callback.message.chat.id

    async def _cancel_order_command(self, message: types.Message, state: FSMContext):
        user_orders = self._orders_storage.get_orders_by_username(str(message.chat.username))
        if len(user_orders) == 0:
            await message.answer(self._text_storage.NO_ACTIVE_ORDER_MESSAGE)
            await state.clear()
            return
        for order in user_orders:
            await print_order(message, order)
        await message.answer(self._text_storage.ASK_FOR_ID_FOR_CANCELLATION)
        await state.set_state(RequestStates.wait_for_id_for_cancel_state)

    async def _process_cancel_order(self, message: types.Message, state: FSMContext):
        order_id = message.text
        _logger.debug(f"Cancel order with id: {order_id}")
        target_order = self._orders_storage.get_order_by_id(order_id)
        if target_order is None:
            await message.answer(self._text_storage.ORDER_NOT_FOUND)
            await state.clear()
            return
        self._entry_processor.process_entry({"action": "CANCEL", "id": order_id, "symbol": target_order.symbol})
        await message.answer(self._text_storage.CANCEL_ORDER_CONFIRMATION)
        await state.clear()

    def _assign_service_fields(self, message: types.Message, data: dict[str, Any]) -> dict[str, Any]:
        """Assign service fields to order data."""
        return {
            **data,
            "id": f"O{self._orders_storage.get_next_order_id}_{data['symbol']}",
            "username": message.chat.username,
        }

    def _get_order_keyboard(self, data: dict[str, Any]) -> InlineKeyboardMarkup:
        """Create an inline keyboard for quick selection."""
        side = data.get("side", "❔")
        symbol = data.get("symbol", "❔")
        price = data.get("price", self._text_storage.REQUEST_FOR_ORDER_PRICE_MESSAGE)
        quantity = data.get("quantity", self._text_storage.REQUEST_FOR_ORDER_QUANTITY_MESSAGE)

        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=f"Side: {side}", callback_data="select_side")],
            [InlineKeyboardButton(text=f"Symbol: {symbol}", callback_data="select_symbol")],
            [InlineKeyboardButton(text=f"💰 {price}", callback_data="enter_price")],
            [InlineKeyboardButton(text=f"📦 {quantity}", callback_data="enter_quantity")],
            [InlineKeyboardButton(text="✅ Confirm Order", callback_data="confirm_order")]
        ])

    @property
    def _side_buttons(self) -> list[list[InlineKeyboardButton]]:
        return [
            [InlineKeyboardButton(text="🟢 Buy", callback_data="set_side:buy"),
             InlineKeyboardButton(text="🔴 Sell", callback_data="set_side:sell")]
        ]

    @property
    def _symbol_buttons(self) -> list[list[InlineKeyboardButton]]:
        return [
            [InlineKeyboardButton(text="GEL/USD", callback_data="set_symbol:GEL/USD"),
             InlineKeyboardButton(text="RUB/USD", callback_data="set_symbol:RUB/USD")]
        ]
