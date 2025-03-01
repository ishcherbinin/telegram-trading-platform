import ast
import asyncio
import logging.config
import os
from pathlib import Path

from aiogram import Bot, Dispatcher

from aiogram.fsm.storage.memory import MemoryStorage

from event_listeners.listeners_manager import ListenersManager
from event_listeners.telegram_event_listener import TgEventListener
from logging_conf import log_config
from telegram_interface.data_converter import TgDataConverter
from telegram_interface.ids_storage import TgIdsStorage
from telegram_interface.message_handler import MessageHandler
from telegram_interface.text_storage import BaseTextStorage
from trading_exchange.exchange_builder import ExchangeBuilder
from trading_exchange.reference_data import ReferenceData

logging.config.dictConfig(log_config)

_logger = logging.getLogger(__name__)

async def update_reference_prices(reference_data: ReferenceData, delay: int) -> None:
    """
    method update reference prices after each hour
    :param delay:
    :param reference_data:
    :return:
    """
    while True:
        reference_data.load_data_api_currency()
        await asyncio.sleep(delay)


async def main() -> None:
    _logger.info("Starting bot")
    all_ids = ast.literal_eval(os.getenv("ALLOWED_IDS", "[]"))
    allowed_chat_ids = [os.getenv("MANAGERS_CHAT"), *all_ids]
    _logger.debug(f"Allowed chat ids: {allowed_chat_ids}")
    api_token = os.getenv("TELEGRAM_API_TOKEN")
    _logger.debug(f"API token: {api_token}")

    available_symbols = os.getenv("AVAILABLE_SYMBOLS", "['RUB/USD','GEL/USD']")

    tables_path = Path(os.getenv("REFERENCE_DATA_TABLES_PATH", "tables"))

    symbols = ast.literal_eval(available_symbols)

    fetch_price_delay = int(os.getenv("FETCH_PRICE_DELAY", 60))

    bot = Bot(token=api_token)
    mem_storage = MemoryStorage()
    dp = Dispatcher(storage=mem_storage)
    text_storage = BaseTextStorage()
    exchange_builder = ExchangeBuilder()
    exchange_builder.build_exchange()
    exchange_builder.reference_data.set_available_symbols(symbols)
    exchange_builder.reference_data.load_ref_data_tables(tables_path)

    ids_storage = TgIdsStorage()
    ids_storage.set_managers_ids(allowed_chat_ids)
    data_converter = TgDataConverter()

    listeners_manager = ListenersManager(listeners=[TgEventListener(bot, ids_storage, text_storage)])

    msg_handler = MessageHandler(bot, dp,
                                 ids_storage,
                                 text_storage,
                                 exchange_builder,
                                 data_converter,
                                 listeners_manager)
    msg_handler.register_handlers()

    try:
        _logger.info("Starting polling")
        asyncio.create_task(update_reference_prices(exchange_builder.reference_data, fetch_price_delay))
        await dp.start_polling(bot)
    except Exception as e:
        _logger.error(f"Error while polling: {e}")
        raise e



if __name__ == "__main__":
    asyncio.run(main())
