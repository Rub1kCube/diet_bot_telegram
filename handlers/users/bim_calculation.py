import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from loader import dp
from data.message_text import TEXT, MAIN_MENU_TEXT, BUTTON_TEXT_START_CALC
from keyboards.reply import menu
from states.calc_bim import CalcBIM
from ..services import calc_IMT, is_float


@dp.message_handler(Text(equals=MAIN_MENU_TEXT[1]))
async def calculate_bim_calculation(message: types.Message):
    logging.info(f'calculate_bim_calculation: user = {message.from_user.id}')
    await message.answer(TEXT['text_bim'], reply_markup=menu.test_start_calc)


@dp.message_handler(Text(equals=BUTTON_TEXT_START_CALC))
async def calculate_bim_test(message: types.Message):
    logging.info(f'calculate_bim_test: user = {message.from_user.id}')
    await message.answer('Введите Ваш реальный вес (в кг):', reply_markup=types.ReplyKeyboardRemove())
    await CalcBIM.first()


@dp.message_handler(state=CalcBIM.BODY_MASS)
async def answer_body_mass_bim(message: types.Message, state: FSMContext):
    answer = message.text
    if not is_float(answer):
        await message.answer("Некорректные ввод данных!")
        return

    logging.info(f'answer_: body_mass_bim={answer}')
    await state.update_data(body_mass=float(answer))
    await message.answer('Введите Ваш реальный рост (в см):', reply_markup=types.ReplyKeyboardRemove())
    await CalcBIM.next()


@dp.message_handler(state=CalcBIM.GROWTH)
async def answer_growth_bim(message: types.Message, state: FSMContext):
    answer = message.text
    if (not answer.isdigit()) or (float(answer) < 100):

        await message.answer("Некорректные ввод данных!")
        return

    logging.info(f'answer_: answer_growth_bim={answer}')
    await state.update_data(growth=float(answer) / 100)

    answers = await state.get_data()
    result = calc_IMT(growth=answers['growth'], body_mass=answers['body_mass'])
    await message.answer(TEXT['result_bim'].format(result),
                         reply_markup=menu.end_daily_norm_menu, parse_mode='Markdown')
    logging.info(f'result_bim: {result}')
    await state.finish()







