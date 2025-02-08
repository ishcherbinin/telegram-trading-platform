import logging
from aiogram import types
from trading_exchange.order import Order

_logger = logging.getLogger(__name__)

async def print_order(message: types.Message, order: Order):
    await message.answer(f"\nID: {order.id}"
                         f"\nUsername: {order.username}"
                         f"\nSymbol: {order.symbol}"
                         f"\nPrice: {order.order_price}"
                         f"\nQuantity: {order.order_qty},"
                         f"\nSide: {order.side.value},"
                         f"\nLeaves qty: {order.leaves_qty},")

async def validate_chat_id(chat_id: str, allowed_chat_ids: list[str]) -> bool:
    _logger.debug(f"Chat id: {chat_id}")
    _logger.debug(f"Allowed chat ids: {allowed_chat_ids}")
    if chat_id not in allowed_chat_ids:
        return True
    return False

