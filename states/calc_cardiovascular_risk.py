from aiogram.dispatcher.filters.state import StatesGroup, State


class CalcCardiovascularRisk(StatesGroup):

    SEX = State()
    AGE = State()
    IS_SMOKING = State()
    ARTERIAL_PRESSURE = State()
    CHOLESTEROL = State()
