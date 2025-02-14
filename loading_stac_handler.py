from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.ECP.stationar import export_stories_function

router = Router()


class LoadingStacHandler(StatesGroup):
    step_1 = State()


@router.message(Command(commands=['stac']))
async def info_loading_stac_handler(message: Message, state: FSMContext):
    await state.set_state(LoadingStacHandler.step_1)
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Да, выгружай', callback_data='stac_1'))
    builder.row(InlineKeyboardButton(text='Нет, ждем остальных', callback_data='stac_0'))
    await message.answer('Истории готовы для выгрузки?', reply_markup=builder.as_markup())


@router.message(LoadingStacHandler.step_1)
async def upload_stac_handler(callback: CallbackQuery, state: FSMContext):
    if callback.data == 'stac_1':
        export_stories_function()
        await callback.message.answer('Истории выгружены, смотри логи')
    elif callback.data == 'stac_0':
        await callback.message.answer('Ждем готовности историй. Как будут готовы отправь снова команду для выгрузки')
    else:
        await callback.message.answer('Что-то пошло не так')
    await state.clear()


