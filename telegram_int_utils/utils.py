import logging

_logger = logging.getLogger(__name__)

async def validate_chat_id(chat_id: str, allowed_chat_ids: list[str]) -> bool:
    _logger.debug(f"Chat id: {chat_id}")
    _logger.debug(f"Allowed chat ids: {allowed_chat_ids}")
    if chat_id not in allowed_chat_ids:
        return True
    return False