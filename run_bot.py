import asyncio
import logging.config
import os

from aiogram import Bot, Dispatcher

from aiogram.fsm.storage.memory import MemoryStorage

from logging_conf import log_config
from telegram_int_utils.data_converter import TgDataConverter
from telegram_int_utils.message_handler import MessageHandler
from telegram_int_utils.text_storage import BaseTextStorage
from trading_exchange.exchange_builder import ExchangeBuilder

logging.config.dictConfig(log_config)

_logger = logging.getLogger(__name__)

async def main() -> None:
    _logger.info("Starting bot")
    allowed_chat_ids = [os.getenv("MANAGERS_CHAT"), *os.getenv("ALLOWED_IDS", [])]
    _logger.debug(f"Allowed chat ids: {allowed_chat_ids}")
    api_token = os.getenv("TELEGRAM_API_TOKEN")
    _logger.debug(f"API token: {api_token}")

    bot = Bot(token=api_token)
    mem_storage = MemoryStorage()
    dp = Dispatcher(storage=mem_storage)
    text_storage = BaseTextStorage()
    exchange_builder = ExchangeBuilder()
    exchange_builder.build_exchange()

    data_converter = TgDataConverter()

    msg_handler = MessageHandler(bot, dp, allowed_chat_ids,
                                 text_storage,
                                 exchange_builder,
                                 data_converter)
    msg_handler.register_handlers()

    try:
        _logger.info("Starting polling")
        await dp.start_polling(bot)
    except Exception as e:
        _logger.error(f"Error while polling: {e}")
        raise e



if __name__ == "__main__":
    asyncio.run(main())
