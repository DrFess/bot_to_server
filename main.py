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
import start_menu_handler
from middleware import AllowedUserMiddleware
from settings import TOKEN, PROXY_URL


session = AiohttpSession(proxy=PROXY_URL)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'), session=session)
# bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))  # для запуска на ноуте


async def scheduler():
    aioschedule.every().day.at('23:45').do(schedule_handler.start_scheduler)  # 07:45
    # aioschedule.every().day.at('10:00').do(hospitalisation_stac_handler.hospitalize)
    aioschedule.every().day.at('21:00').do(hospitalisation_stac_handler.hospitalize_new)  # 05:00
    aioschedule.every().day.at('08:00').do(hospitalisation_stac_handler.hospitalize_new)  # 16:00
    aioschedule.every().day.at('10:00').do(hospitalisation_stac_handler.operation_update)  # 18:00
    # aioschedule.every().day.at('22:30').do(hospitalisation_stac_handler.operation_update)  # 06:30
    aioschedule.every().day.at('12:00').do(hospitalisation_stac_handler.extract_patients)  # 20:00
    # aioschedule.every().day.at('23:00').do(hospitalisation_stac_handler.extract_patients)  # 07:00

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

    asyncio.create_task(scheduler())
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
