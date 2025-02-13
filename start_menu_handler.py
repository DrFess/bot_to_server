from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

router = Router()


@router.message(Command(commands=['start']))
async def command_start_handler(message: Message):
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text='Отправить отчет по травмпункту'))
    await message.answer(
        'Привет, я - бот и живу в больнице. Чем могу помочь смотри в Меню',
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@router.message()
async def echo_message(message: Message):
    await message.answer(message.text)
