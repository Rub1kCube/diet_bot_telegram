from aiogram.dispatcher.filters.state import StatesGroup, State


class CalcBIM(StatesGroup):

    BODY_MASS = State()
    GROWTH = State()
