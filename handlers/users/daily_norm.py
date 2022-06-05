import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from loader import dp
from data.message_text import TEXT, MAIN_MENU_TEXT, BUTTON_TEXT_START
from keyboards.reply import menu
from keyboards.inline import link_button
from states.calc_daily_norm import CalcDailyNormTest

from ..services import (
    correct_sex, correct_age, CalcDailyNorm,
    correct_kfa, convert_age, convert_kfa,
    convert_sex, is_float,
)


@dp.message_handler(Command('start'))
async def show_menu(message: types.Message):
    await message.answer(TEXT['text_hi'], reply_markup=menu.main_menu, parse_mode='Markdown')
    await message.answer(TEXT['link_stickers'], reply_markup=link_button.keyboard)


@dp.message_handler(Text(equals=MAIN_MENU_TEXT[0]))
async def calculate_daly_norm(message: types.Message):
    logging.info(f'calculate_daly_norm: user = {message.from_user.id}')
    await message.answer(TEXT['calorie_calculation'], reply_markup=menu.test_start)


@dp.message_handler(Text(equals=BUTTON_TEXT_START))
async def calculate_daly_norm_test(message: types.Message):
    logging.info(f'calculate_daly_norm_test: user = {message.from_user.id}')
    await message.answer('Ваш пол?', reply_markup=menu.sex_menu)
    await CalcDailyNormTest.first()


@dp.message_handler(state=CalcDailyNormTest.SEX)
async def answer_sex(message: types.Message, state: FSMContext):
    answer = message.text
    if not correct_sex(answer):
        await message.answer("Пожалуйста, выберите пол, используя клавиатуру ниже!")
        return

    logging.info(f'answer_sex: sex={answer}')
    answer = convert_sex(answer)
    await state.update_data(sex=answer)
    await message.answer('Ваш возраст?', reply_markup=menu.age_menu)
    await CalcDailyNormTest.next()


@dp.message_handler(state=CalcDailyNormTest.AGE)
async def answer_age(message: types.Message, state: FSMContext):
    answer = message.text
    if not correct_age(answer):
        await message.answer("Пожалуйста, выберите возраст, используя клавиатуру ниже!")
        return
    logging.info(f'answer_age: age={answer}')

    answer = convert_age(answer)
    await state.update_data(age=answer)
    await message.answer('Ваша реальная масса тела в кг?', reply_markup=types.ReplyKeyboardRemove())
    await CalcDailyNormTest.next()


@dp.message_handler(state=CalcDailyNormTest.BODY_MASS)
async def answer_body_mass(message: types.Message, state: FSMContext):
    answer = message.text
    if not is_float(answer):
        await message.answer("Некорректные ввод данных!")
        return
    logging.info(f'answer_body_mass: body_mass={answer}')

    await state.update_data(body_mass=float(answer))
    await message.answer('Реальный уровень вашей физической подготовки?', reply_markup=menu.active_menu)
    await CalcDailyNormTest.next()


@dp.message_handler(state=CalcDailyNormTest.ACTIVE)
async def answer_active(message: types.Message, state: FSMContext):

    answer = message.text
    if not correct_kfa(answer):
        await message.answer("Пожалуйста, выберите ответ, используя клавиатуру ниже!")
        return
    answer = convert_kfa(answer)
    await state.update_data(kfa=answer)

    answers = await state.get_data()
    result = CalcDailyNorm(**answers)
    logging.info(f'answer_active: active={answer}')

    await message.answer(TEXT['result_daily_norm'].format(result.calc_daily_calories()),
                         reply_markup=menu.end_daily_norm_menu, parse_mode='Markdown')
    logging.info(f'result: {result.calc_daily_calories()}')
    await state.finish()
