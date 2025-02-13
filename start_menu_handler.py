from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message

router = Router()


@router.message(Command(commands=['start']))
async def command_start_handler(message: Message):
    await message.answer('Привет, я - бот для детского травмпункта.')


@router.message()
async def echo_message(message: Message):
    await message.answer(message.text)
