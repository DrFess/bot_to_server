from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from utils.ECP.stationar_v2 import working_with_stories

router = Router()


@router.message(Command(commands=['hospitalize']))
async def hospitalize(message: Message):
    working_with_stories()
