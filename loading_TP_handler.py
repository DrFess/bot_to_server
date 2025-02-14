from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.L2.loading_tp_statistical_card import upload_statistic_card_from_ECP

router = Router()


class LoadingHandler(StatesGroup):
    step_1 = State()
    step_2 = State()


@router.message(Command(commands=['upload']))
async def info_loading_handler(message: Message, state: FSMContext):
    await state.set_state(LoadingHandler.step_1)
    await message.answer('отправь мне файл с расширением .xslx\n '
                         'Проверь чтобы дата в название файла была полной (в формате дд.мм.гггг.)\n'
                         'Так же должно быть указано Первично или Повторно')


@router.message(LoadingHandler.step_1)
async def get_file(message: Message, state: FSMContext):
    await message.bot.download(file=message.document.file_id, destination=f'table/{message.document.file_name}')
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text='Да', callback_data='1'))
    builder.row(InlineKeyboardButton(text='Нет', callback_data='0'))
    await message.answer('Отчет загружен, выгрузить в ЕЦП', reply_markup=builder.as_markup())
    await state.set_state(LoadingHandler.step_2)


@router.callback_query(LoadingHandler.step_2)
async def loading_patients(callback: CallbackQuery, state: FSMContext):
    if callback.data == '1':
        await callback.message.answer('Начал выгружать в ЕЦП')
        upload_statistic_card_from_ECP()
        await callback.message.answer('Закончил выгружать в ЕЦП')
    elif callback.data == '0':
        await callback.message.answer('Отчет удален. Для запуска процедуры выгрузки статталона используй команду из меню')
    else:
        await callback.message.answer('Что-то пошло не так')
    await state.clear()
