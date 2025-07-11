import requests
from aiogram import Router
from aiogram.filters import Command

from main import bot
from settings import proxies, admin
from utils.ECP.stationar_v2 import working_with_stories
from utils.ECP.stationar_v3 import add_patients_in_ecp, add_operation, discharge_patient

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


@router.message(Command(commands=['hospitalize_new']))
async def hospitalize_new():
    session = requests.Session()  # создание сессии подключения
    session.proxies.update(proxies)
    message = add_patients_in_ecp(session)
    session.close()
    await bot.send_message(chat_id=admin, text=message)


@router.message(Command(commands=['operation_update']))
async def operation_update():
    session = requests.Session()
    session.proxies.update(proxies)
    message = add_operation(session)
    session.close()
    await bot.send_message(chat_id=admin, text=message)


@router.message(Command(commands=['extract']))
async def extract_patients():
    session = requests.Session()
    session.proxies.update(proxies)
    message = discharge_patient(session)
    session.close()
    await bot.send_message(chat_id=admin, text=message)
