from aiogram import types
from aiogram.dispatcher.filters import Text

from data.message_text import MENU_END_DAILY_NORM, TEXT, MENU_PROTEINS_FATS
from keyboards.reply import menu
from loader import dp


@dp.message_handler(Text(equals=MENU_END_DAILY_NORM[1]))
async def redirect_start_menu(message: types.Message):
    await message.answer('Вы в главном меню', reply_markup=menu.main_menu)


@dp.message_handler(Text(equals=MENU_END_DAILY_NORM[0]))
async def recomendation_menu(message: types.Message):
    await message.answer(TEXT['proteins_fats'], reply_markup=menu.proteins_fats_menu, parse_mode='Markdown')


@dp.message_handler(Text(equals=MENU_PROTEINS_FATS[0]))
async def protein_answer(message: types.Message):
    await message.answer(TEXT['protein'], parse_mode='Markdown')


@dp.message_handler(Text(equals=MENU_PROTEINS_FATS[1]))
async def fats_answer(message: types.Message):
    await message.answer(TEXT['fats'], parse_mode='Markdown')
