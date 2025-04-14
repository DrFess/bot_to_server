from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

router = Router()


@router.message(Command(commands=['hospitalize']))
async def hospitalize(message: Message, state: FSMContext):
    working_with_stories()