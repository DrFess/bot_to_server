import requests
from aiogram import Router
from aiogram.filters import Command

from main import bot
from settings import proxies, admin
from utils.ECP.stationar_v2 import working_with_stories

router = Router()


@router.message(Command(commands=['hospitalize']))
async def hospitalize():
    session = requests.Session()  # создание сессии подключения
    session.proxies.update(proxies)
    try:
        working_with_stories(session)
    except Exception as error:
        await bot.send_message(chat_id=admin, text=error)
    session.close()
