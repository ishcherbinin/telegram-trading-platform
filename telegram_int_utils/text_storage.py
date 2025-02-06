
class BaseTextStorage:

    """
    Class contains enums for text messages in tg bot,
    If it is required to change texts, provide another storage in runner of the bot
    Make sure you use same enum names
    """

    COMMON_GREETING = "Hello! I am trading bot, I can help you with trading operations"

    HELP_CLIENT = f"""
    {COMMON_GREETING}
    
    /help - show help message with available commands
    /myorders - show all your orders based on user name
    /cancelorder - cancel order by order id
    /neworder - create new order (specify symbol, side, price, quantity)
    /currentsession - show current trading session for instrument
    /exit - exit from current state
    """

    HELP_MANAGERS = f"""
    {COMMON_GREETING}
    
    /help - show help message with available commands
    /showallorders - show all orders in the system
    /cancelorder - cancel order by order id
    /currentsession - show current trading session for instrument
    /getid - get chat id
    /exit - exit from current state
    """


    CHAT_ID_MESSAGE = "Your chat id is"

    NO_ACTIVE_ORDER_MESSAGE = "No active orders in the system"

    TEXT_NO_PERMISSIONS_FOR_COMMAND = "You are not allowed to use this command"

    REQUEST_FOR_SYMBOL_FOR_SESSION_CHECK = "Please provide symbol for session check"

    TEXT_CURRENT_SESSION_ON_INSTRUMENT = "Current session is "