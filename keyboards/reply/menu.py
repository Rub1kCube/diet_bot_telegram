from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from data.message_text import MAIN_MENU_TEXT

main_menu = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)

for button in MAIN_MENU_TEXT:
    main_menu.insert(
        KeyboardButton(
            text=button,
        )
    )
