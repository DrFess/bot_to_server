from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

from settings import admin
from utils.L2.diaries import create_diaries_function

router = Router()


@router.message(Command(commands=['scheduler']))
async def start_scheduler(message: Message):
    await message.bot.send_message(chat_id=admin, text='Запущен процесс создания дневников')
    if create_diaries_function():
        await message.bot.send_message(chat_id=admin, text='Дневники созданы, проверяй')
    else:
        await message.bot.send_message(chat_id=admin, text='Что-то пошло не так')
