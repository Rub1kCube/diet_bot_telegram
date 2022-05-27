from typing import Union

from aiogram import types
from aiogram.dispatcher.filters import Command, Text

from loader import dp
from data.message_text import TEXT, MAIN_MENU_TEXT
from keyboards.reply import menu


@dp.message_handler(Command('start'))
async def show_menu(message: types.Message):
    await message.answer(TEXT['text_hi'], reply_markup=menu.main_menu, parse_mode='Markdown')


@dp.message_handler(Text(equals=MAIN_MENU_TEXT[0]))
async def calculate_daly_norm(message: types.Message):
    pass



