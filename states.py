from aiogram.fsm.state import StatesGroup, State


class AddUrl(StatesGroup):
    enter_urlname = State()
    enter_url = State()
