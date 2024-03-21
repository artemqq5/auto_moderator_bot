from aiogram.fsm.state import StatesGroup, State


class StateDeleteChannel(StatesGroup):
    permission = State()
