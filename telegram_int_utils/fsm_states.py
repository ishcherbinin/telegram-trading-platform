from aiogram.fsm.state import State, StatesGroup

class RequestStates(StatesGroup):

    """
    Class contains states for different requests
    """


    wait_for_symbol_for_session_state = State()