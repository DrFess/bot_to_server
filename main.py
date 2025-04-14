import asyncio
import logging

import aioschedule
from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

import hospitalisation_stac_handler
import loading_TP_handler
import loading_stac_handler
import schedule_handler
from schedule_handler import start_scheduler
import start_menu_handler
from middleware import AllowedUserMiddleware
from settings import TOKEN, PROXY_URL


async def scheduler():
    aioschedule.every().day.at('23:45').do(start_scheduler)

    while True:
        await aioschedule.run_pending()
        await asyncio.sleep(1)


async def main():
    dp = Dispatcher()
    dp.message.middleware(AllowedUserMiddleware())
    dp.include_routers(
        start_menu_handler.router,
        loading_TP_handler.router,
        loading_stac_handler.router,
        schedule_handler.router,
        hospitalisation_stac_handler.router
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
