from aiogram.fsm.state import StatesGroup, State


class ClientState(StatesGroup):
    start = State()
    full_name = State()
    birth_date = State()
