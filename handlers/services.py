from enum import Enum


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


def calc_daily_calories(age: int, body_mass: float, cfa: KFA, sex: Sex = Sex.HUMAN) -> float:
    """Расчёт суточной калорийности"""

    if age < Age.YOUNG.value:
        raise ValueError('The number must be equal to or greater than 18')

    if body_mass < 10:
        raise ValueError('Body weight cannot be less than 10 kg')

    if Age.YOUNG.value <= age < Age.ADULT.value:
        multiplication_factor, plus_factor = (0.0621, 2.0357) if sex == Sex.HUMAN else (0.0630, 2.8957)
    elif Age.ADULT.value <= age < Age.PENSIONER.value:
        multiplication_factor, plus_factor = (0.0342, 3.5377) if sex == Sex.HUMAN else (0.0484, 3.6534)
    else:
        multiplication_factor, plus_factor = (0.0377, 2.7545) if sex == Sex.HUMAN else (0.0491, 2.4587)

    return round((multiplication_factor * body_mass + plus_factor) * 240 * cfa.value, ndigits=2)


def calc_IMT(growth: float, body_mass: float):
    """Расчёт ИМТ"""

    if body_mass < 10:
        raise ValueError('Body weight cannot be less than 10 kg')

    if not 0.9 < growth < 3.0:
        raise ValueError('Height less than 0.9 is not valid')

    return round(body_mass / (growth ** 2), ndigits=2)

