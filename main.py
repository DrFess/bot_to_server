import asyncio
import logging

import aioschedule
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

import start_menu_handler
from middleware import AllowedUserMiddleware
from settings import TOKEN, PROXY_URL
from utils.L2.diaries import create_diaries_function


async def scheduler():
    aioschedule.every().day.at('23:45').do(create_diaries_function)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    dp = Dispatcher()
    dp.message.middleware(AllowedUserMiddleware())
    dp.include_routers(
        start_menu_handler.router,
    )
    session = AiohttpSession(proxy=PROXY_URL)
    asyncio.create_task(scheduler())
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'), session=session)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
