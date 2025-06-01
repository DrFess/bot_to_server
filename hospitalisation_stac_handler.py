import requests
from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from settings import proxies
from utils.ECP.stationar_v2 import working_with_stories

router = Router()


@router.message(Command(commands=['hospitalize']))
async def hospitalize():
    session = requests.Session()  # создание сессии подключения
    session.proxies.update(proxies)
    working_with_stories(session)
    session.close()
