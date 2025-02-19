from aiogram.fsm.state import State, StatesGroup

class RequestStates(StatesGroup):

    """
    Class contains states for different requests
    """

    wait_for_symbol_for_reference_price_state = State()
    wait_for_symbol_for_session_change = State()
    wait_for_order_quantity = State()
    wait_for_order_price = State()
    wait_for_order_details = State()
    wait_for_symbol_for_session_state = State()
    wait_for_id_for_cancel_state = State()
    wait_for_symbol_for_new_order = State()
