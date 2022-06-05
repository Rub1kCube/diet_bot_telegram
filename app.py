import logging

from loader import bot, storage


async def on_shutdown(dp):
    await bot.close()
    await storage.close()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    logging.basicConfig(level=logging.INFO)
    executor.start_polling(dp, on_shutdown=on_shutdown)
