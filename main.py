import asyncio
import logging

import aioschedule
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

import loading_TP_handler
import loading_stac_handler
import start_menu_handler
from middleware import AllowedUserMiddleware
from settings import TOKEN, PROXY_URL
from utils.L2.diaries import create_diaries_function


async def scheduler():
    aioschedule.every().day.at('13:17').do(run_create_diaries_task)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def run_create_diaries_task():
    task = asyncio.create_task(create_diaries_function())
    try:
        await task
    except Exception as e:
        logging.error(f"Ошибка при выполнении create_diaries_function: {e}")


async def main():
    dp = Dispatcher()
    dp.message.middleware(AllowedUserMiddleware())
    dp.include_routers(
        start_menu_handler.router,
        loading_TP_handler.router,
        loading_stac_handler.router
    )
    session = AiohttpSession(proxy=PROXY_URL)
    asyncio.create_task(scheduler())
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'), session=session)
    # bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
