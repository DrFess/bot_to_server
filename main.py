import asyncio
import logging

from aiogram import Bot, Dispatcher, Router, F
from aiogram.client.default import DefaultBotProperties
from aiogram.filters import Command
from aiogram.types import Message
from aiohttp import ProxyConnector

from settings import TOKEN, PROXY_URL

connector = ProxyConnector.from_url(PROXY_URL)
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'), connector=connector)
router = Router()


@router.message(Command(commands=['start']))
async def command_start_handler(message: Message):
    await message.answer('Привет, я - бот для детского травмпункта.')


@router.message()
async def echo_message(message: Message):
    await message.answer(message.text)


async def main():
    dp = Dispatcher()
    dp.include_routers(
        router,
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
