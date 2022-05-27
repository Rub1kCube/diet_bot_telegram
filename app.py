import logging

from aiogram import executor

from loader import dp
import handlers


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp)
