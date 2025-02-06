class AbstractTextStorage:


    """
    Class which defines enums required to store text messages for telegram bot
    """

    COMMON_GREETING = ""
    HELP_CLIENT = ""
    HELP_MANAGERS = ""



class TextStorage(AbstractTextStorage):

    """
    Class contains enums for text messages in tg bot,
    If it is required to change texts, provide another storage in runner of the bot
    Make sure you use same enum names
    """

    COMMON_GREETING = "Hello! I am trading bot, I can help you with trading operations"

    HELP_CLIENT = f"""
    {COMMON_GREETING}
    
    /help - show help message with available commands
    /my-orders - show all your orders based on user name
    /cancel-order - cancel order by order id
    /new-order - create new order (specify symbol, side, price, quantity)
    /current-session - show current trading session for instrument
    /exit - exit from current state
    """

    HELP_MANAGERS = f"""
    {COMMON_GREETING}
    
    /help - show help message with available commands
    /show-all-orders - show all orders in the system
    /cancel-order - cancel order by order id
    /current-session - show current trading session for instrument
    /exit - exit from current state
    """

