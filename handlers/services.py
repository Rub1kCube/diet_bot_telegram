from typing import Union
from enum import Enum
import re

from data import message_text
from data.config import calc_cardiovascular_dict


class Age(Enum):
    YOUNG = 18
    ADULT = 31
    PENSIONER = 60


class KFA(Enum):
    SEDENTARY = 1.2
    MORE_ACTIVE = 1.375
    REGULARLY_ENGAGED = 1.55
    PLAYING_SPORTS = 1.725
    PROFESSIONAL_ATHLETES = 1.9


class Sex(Enum):
    HUMAN = 1
    WOMAN = 2


class CalcDailyNorm:

    def __init__(self, sex: Sex, age: Age, body_mass: int, kfa: KFA):
        self.sex = sex
        self.age = age
        self.body_mass = body_mass
        self.kfa = kfa

    def calc_daily_calories(self) -> float:
        """Расчёт суточной калорийности"""

        if self.body_mass < 10:
            raise ValueError('Body weight cannot be less than 10 kg')

        if Age.YOUNG:
            multiplication_factor, plus_factor = (0.0621, 2.0357) if self.sex == Sex.HUMAN else (0.0630, 2.8957)
        elif Age.ADULT:
            multiplication_factor, plus_factor = (0.0342, 3.5377) if self.sex == Sex.HUMAN else (0.0484, 3.6534)
        else:
            multiplication_factor, plus_factor = (0.0377, 2.7545) if self.sex == Sex.HUMAN else (0.0491, 2.4587)

        return round((multiplication_factor * self.body_mass + plus_factor) * 240 * self.kfa.value, ndigits=2)


def calc_cardiovascular(arterial_pressure: int, is_smoking: bool, age: int, cholesterol: int, sex: Sex) -> float:
    """Расчёт по SCORE"""

    arterial_pressure_list = [120, 140, 160, 180]

    if sex.HUMAN and is_smoking:
        result = calc_cardiovascular_dict[Sex.HUMAN.value][is_smoking][age][cholesterol][arterial_pressure_list.index(
            arterial_pressure)]
    elif sex.HUMAN and not is_smoking:
        result = calc_cardiovascular_dict[Sex.HUMAN.value][is_smoking][age][cholesterol][arterial_pressure_list.index(
            arterial_pressure)]
    elif sex.WOMAN and is_smoking:
        result = calc_cardiovascular_dict[Sex.WOMAN.value][is_smoking][age][cholesterol][arterial_pressure_list.index(
            arterial_pressure)]
    else:
        result = calc_cardiovascular_dict[Sex.WOMAN.value][is_smoking][age][cholesterol][arterial_pressure_list.index(
            arterial_pressure)]

    return result


def calc_IMT(growth: float, body_mass: float) -> float:
    """Расчёт ИМТ"""
    return round(body_mass / (growth ** 2), ndigits=2)


def correct_sex(message: str) -> bool:
    if message in message_text.SEX_TEXT_KEYBOARD:
        return True
    return False


def correct_age_cardiovascular(message: str) -> bool:

    if message in message_text.MENU_AGE_CARDIOVASCULAR:
        return True

    return False


def correct_arterial_pressure(message: str) -> bool:
    if message in message_text.MENU_ARTERIAL_PRESSURE:
        return True
    return False


def correct_cholesterol(message: str) -> bool:
    if message in message_text.MENU_CHOLESTEROL:
        return True
    return False


def correct_is_smoking(message: str) -> bool:
    if message in message_text.MENU_SMOKING:
        return True
    return False


def correct_age(message: str) -> bool:
    if message in message_text.MENU_AGE:
        return True
    return False


def correct_kfa(message: str) -> bool:
    if message in message_text.MENU_ACTIVE:
        return True
    return False


def convert_age(age: str) -> Union[None, Age]:
    try:
        index = message_text.MENU_AGE.index(age)
    except ValueError:
        return

    #  TODO переписать этот костыль на нормальный код
    if index == 0:
        return Age.YOUNG
    elif index == 1:
        return Age.ADULT
    else:
        return Age.PENSIONER


def convert_sex(sex: str) -> Union[None, Sex]:
    try:
        index = message_text.SEX_TEXT_KEYBOARD.index(sex)
    except ValueError:
        return

    #  TODO переписать этот костыль на нормальный код
    if index == 0:
        return Sex.HUMAN
    else:
        return Sex.WOMAN


def convert_kfa(kfa: str) -> Union[None, KFA]:
    try:
        index = message_text.MENU_ACTIVE.index(kfa)
    except ValueError:
        return

    #  TODO переписать этот костыль на нормальный код
    if index == 0:
        return KFA.SEDENTARY
    elif index == 1:
        return KFA.MORE_ACTIVE
    elif index == 2:
        return KFA.REGULARLY_ENGAGED
    elif index == 3:
        return KFA.PLAYING_SPORTS
    else:
        return KFA.PROFESSIONAL_ATHLETES


def convert_arterial_pressure(message: str) -> int:
    arterial_pressure_list = [120, 140, 160, 180]
    index = message_text.MENU_ARTERIAL_PRESSURE.index(message)
    return arterial_pressure_list[index]


def convert_cholesterol(message: str) -> int:
    cholesterol_list = [4, 5, 6, 7, 8]
    index = message_text.MENU_CHOLESTEROL.index(message)
    return cholesterol_list[index]


def convert_age_cardiovascular(message: str) -> int:
    age_list = [40, 45, 55, 60]
    index = message_text.MENU_AGE_CARDIOVASCULAR.index(message)
    return age_list[index]


def convert_is_smoking(message: str) -> bool:
    return message == message_text.MENU_SMOKING[0]


def is_float(text: str) -> bool:
    if re.fullmatch(r'(\d+\.\d+)|(\d+)', text) is not None:
        return True
    return False
