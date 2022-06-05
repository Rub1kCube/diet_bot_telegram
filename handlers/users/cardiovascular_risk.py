import logging

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from handlers.services import (
    correct_sex, convert_sex, correct_arterial_pressure,
    correct_age_cardiovascular, correct_is_smoking,
    convert_arterial_pressure, correct_cholesterol,
    convert_cholesterol, convert_age_cardiovascular,
    calc_cardiovascular, convert_is_smoking,
)
from loader import dp
from data.message_text import TEXT, MAIN_MENU_TEXT, BUTTON_TEXT_START_TWO
from keyboards.reply import menu
from states.calc_cardiovascular_risk import CalcCardiovascularRisk


@dp.message_handler(Text(equals=MAIN_MENU_TEXT[2]))
async def calculate_cardiovascular(message: types.Message):
    logging.info(f'calculate_cardiovascular: user = {message.from_user.id}')
    await message.answer(TEXT['cardiovascular'], reply_markup=menu.test_start_two)


@dp.message_handler(Text(equals=BUTTON_TEXT_START_TWO))
async def calculate_cardiovascular_test(message: types.Message):
    logging.info(f'calculate_daly_norm_test: user = {message.from_user.id}')
    await message.answer('Ваш пол?', reply_markup=menu.sex_menu)
    await CalcCardiovascularRisk.first()


@dp.message_handler(state=CalcCardiovascularRisk.SEX)
async def answer_sex_cardiovascular(message: types.Message, state: FSMContext):
    answer = message.text
    if not correct_sex(answer):
        await message.answer("Пожалуйста, выберите пол, используя клавиатуру ниже!")
        return

    logging.info(f'answer_sex: sex={answer}')
    answer = convert_sex(answer)
    await state.update_data(sex=answer)
    await message.answer('Ваш возраст?', reply_markup=menu.age_cardiovascular)
    await CalcCardiovascularRisk.next()


@dp.message_handler(state=CalcCardiovascularRisk.AGE)
async def answer_age_cardiovascular(message: types.Message, state: FSMContext):
    answer = message.text
    if not correct_age_cardiovascular(answer):
        await message.answer("Пожалуйста, выберите возраст, используя клавиатуру ниже!")
        return
    logging.info(f'answer_age_cardiovascular: age={answer}')

    answer = convert_age_cardiovascular(answer)
    print(answer)
    await state.update_data(age=answer)
    await message.answer('Вы курите?', reply_markup=menu.smoking_menu)
    await CalcCardiovascularRisk.next()


@dp.message_handler(state=CalcCardiovascularRisk.IS_SMOKING)
async def answer_smoking(message: types.Message, state: FSMContext):
    answer = message.text
    print(answer)
    if not correct_is_smoking(answer):
        await message.answer("Не корректный ответ!")
        return
    logging.info(f'answer_age_cardiovascular: age={answer}')

    answer = convert_is_smoking(answer)
    await state.update_data(is_smoking=answer)
    await message.answer('Ваше систолическое (верхнее) артериальное давление?',
                         reply_markup=menu.menu_arterial_pressure)
    await CalcCardiovascularRisk.next()


@dp.message_handler(state=CalcCardiovascularRisk.ARTERIAL_PRESSURE)
async def answer_arterial_pressure(message: types.Message, state: FSMContext):
    answer = message.text
    if not correct_arterial_pressure(answer):
        await message.answer("Не корректный ответ!")
        return
    logging.info(f'answer_age_cardiovascular: age={answer}')

    answer = convert_arterial_pressure(answer)
    await state.update_data(arterial_pressure=answer)
    await message.answer('Ваш уровень общего холестерина?', reply_markup=menu.cholesterol_menu)
    await CalcCardiovascularRisk.next()


@dp.message_handler(state=CalcCardiovascularRisk.CHOLESTEROL)
async def answer_cholesterol(message: types.Message, state: FSMContext):
    answer = message.text
    if not correct_cholesterol(answer):
        await message.answer("Не корректный ответ!")
        return
    logging.info(f'answer_age_cardiovascular: age={answer}')

    answer = convert_cholesterol(answer)
    await state.update_data(cholesterol=answer)

    answers = await state.get_data()
    result = calc_cardiovascular(**answers)
    logging.info(f'result: {result}')
    await message.answer(f'Результат: {result}%\n\n{TEXT["cardiovascular_result"]}', reply_markup=menu.main_menu)
    await CalcCardiovascularRisk.next()



