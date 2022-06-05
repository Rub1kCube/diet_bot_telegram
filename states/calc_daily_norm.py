from aiogram.dispatcher.filters.state import StatesGroup, State


class CalcDailyNormTest(StatesGroup):

    SEX = State()
    AGE = State()
    BODY_MASS = State()
    ACTIVE = State()