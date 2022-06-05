from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from typing import List

from data.message_text import (
    MAIN_MENU_TEXT, BUTTON_TEXT_START,
    SEX_TEXT_KEYBOARD, MENU_ACTIVE,
    MENU_AGE, MENU_END_DAILY_NORM,
    MENU_PROTEINS_FATS, BUTTON_TEXT_START_CALC,
    BUTTON_TEXT_START_TWO, MENU_SMOKING,
    MENU_CHOLESTEROL, MENU_AGE_CARDIOVASCULAR,
    MENU_ARTERIAL_PRESSURE
)

main_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
sex_menu = ReplyKeyboardMarkup(row_width=2, resize_keyboard=True)
active_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
age_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
end_daily_norm_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
proteins_fats_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
smoking_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
cholesterol_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
menu_arterial_pressure = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
age_cardiovascular = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

test_start = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).insert(KeyboardButton(text=BUTTON_TEXT_START))
test_start_two = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).insert(
    KeyboardButton(text=BUTTON_TEXT_START_TWO)
)
test_start_calc = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).insert(
    KeyboardButton(text=BUTTON_TEXT_START_CALC)
)


def create_menu(menu: ReplyKeyboardMarkup, titles: List[str]) -> None:

    for title in titles:
        menu.insert(
            KeyboardButton(
                text=title
            )
        )


create_menu(smoking_menu, MENU_SMOKING)
create_menu(cholesterol_menu, MENU_CHOLESTEROL)
create_menu(menu_arterial_pressure, MENU_ARTERIAL_PRESSURE)
create_menu(age_cardiovascular, MENU_AGE_CARDIOVASCULAR)
create_menu(main_menu, MAIN_MENU_TEXT)
create_menu(sex_menu, SEX_TEXT_KEYBOARD)
create_menu(active_menu, MENU_ACTIVE)
create_menu(age_menu, MENU_AGE)
create_menu(end_daily_norm_menu, MENU_END_DAILY_NORM)
create_menu(proteins_fats_menu, MENU_PROTEINS_FATS)

