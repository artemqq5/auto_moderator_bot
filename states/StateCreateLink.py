from aiogram.fsm.state import StatesGroup, State


class StateCreateLink(StatesGroup):
    name_of_link = State()
    hello_message_from_bot = State()
    final_view = State()

