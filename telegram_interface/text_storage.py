
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
    /getreferenceprice - get reference price for symbol
    /currentsession - show current trading session for instrument
    /exit - exit from current state
    """

    HELP_MANAGERS = f"""
    {COMMON_GREETING}
    
    /help - show help message with available commands
    /showallorders - show all orders in the system
    /cancelorder - cancel order by order id
    /neworder - create new order (specify symbol, side, price, quantity)
    /currentsession - show current trading session for instrument
    /getreferenceprice - get reference price for symbol
    /changesession - change session for instrument
    /getid - get chat id
    /exit - exit from current state
    """


    CHAT_ID_MESSAGE = "Your chat id is"

    TEXT_EXIT_MESSAGE = "You have exited from current state"

    NO_ACTIVE_ORDER_MESSAGE = "No active orders in the system"

    TEXT_NO_PERMISSIONS_FOR_COMMAND = "You are not allowed to use this command"

    TEXT_CURRENT_SESSION_ON_INSTRUMENT = "Current session is"

    REQUEST_FOR_ORDER_DETAILS_MESSAGE = "Please provide symbol, side, price, quantity"

    FILL_ORDER_DETAILS_REQUEST_MESSAGE = "🛒 **Fill in your order details:**"

    FILL_SESSION_CHANGE_DETAILS_REQUEST_MESSAGE = "🛒 **Fill in your request details:**"

    REQUEST_FOR_ORDER_PRICE_MESSAGE = "💰 Enter price:"

    REQUEST_FOR_ORDER_QUANTITY_MESSAGE = "📦 Enter quantity:"

    WARNING_FOR_EMPTY_FIELDS = "⚠️ Please complete all fields before confirming."

    CONFIRMATION_OF_ORDER_CREATION_MESSAGE = "✅ Order created successfully."

    ASK_FOR_ID_FOR_CANCELLATION = "🆔 Enter order ID to cancel:"

    CANCEL_ORDER_CONFIRMATION = "✅ Order canceled successfully."

    ORDER_NOT_FOUND = "❌ Order not found."

    REQUEST_FOR_SESSION_CHANGE_PARAMETERS = "🔄 Enter session change parameters:"

    HALT_SESSION_ORDER_REJECTION = "❌ Order rejected. Trading session is halted."

    SUCCESSFUL_SESSION_CHANGE = "✅ Session changed successfully."

    SESSION_CHANGE_NOTIFICATION = "🔄 Session changed for {symbol} to {session}."

    MANAGERS_NOTIFICATION_ABOUT_TRADE = ("📈 New trade happened: "
                                         "\nID: {trade_id} "
                                         "\nSymbol: {symbol} "
                                         "\nPrice: {trade_price} "
                                         "\nQuantity: {trade_qty} "
                                         "\nbetween {passive_username} and {aggressive_username}")

    USER_TRADE_NOTIFICATION = "Trade happened with your order at price {trade_price} and quantity {trade_qty}"

    COMMON_REQUEST_FOR_SYMBOL_ENTITY = "🔍 Enter symbol for request. Available symbols: {symbols}"

    REFERENCE_FOR_SYMBOL_REPLY = "Reference price for {symbol} is {price}"

    ORDER_REJECTION_BY_VALIDATION_TEXT = "Order rejected by validation: {validation_errors}"

    ANY_MESSAGE_ENTRY_TEXT = "This command is not in the list of allowed commands"