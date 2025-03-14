from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, InlineKeyboardButton, CallbackQuery
from aiogram.utils.keyboard import InlineKeyboardBuilder

from utils.L2.loading_tp_statistical_card import upload_statistic_card_from_ECP, delete_statistic_card, \
    validation_table_file_title

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
    if message.document:
        file_name = message.document.file_name
        if validation_table_file_title(file_name):
            await message.bot.download(file=message.document.file_id, destination=f'table/{file_name}')
            await state.update_data(file_name=file_name)
            builder = InlineKeyboardBuilder()
            builder.row(InlineKeyboardButton(text='Да', callback_data='1'))
            builder.row(InlineKeyboardButton(text='Нет', callback_data='0'))
            await message.answer(f'Отчет {message.document.file_name} загружен, выгрузить в ЕЦП', reply_markup=builder.as_markup())
            await state.set_state(LoadingHandler.step_2)
        else:
            await message.answer('Файл не прошёл проверку. Проверь название и отправь корректный файл')
    else:
        await message.answer('Ещё раз: отправь мне файл с расширением .xslx\n '
                             'Проверь чтобы дата в название файла была полной (в формате дд.мм.гггг.)\n'
                             'Так же должно быть указано Первично или Повторно')


@router.callback_query(LoadingHandler.step_2)
async def loading_patients(callback: CallbackQuery, state: FSMContext):
    file_name = await state.get_data()

    if callback.data == '1':
        await callback.message.answer('Начал выгружать в ЕЦП')
        upload_statistic_card_from_ECP()
        await callback.message.answer('Закончил выгружать в ЕЦП')
    elif callback.data == '0':
        await callback.message.answer(f'Отчет {file_name.get('file_name')} удален. Для запуска процедуры выгрузки статталона используй команду из меню')
    else:
        await callback.message.answer('Что-то пошло не так')

    delete_statistic_card(path='table/', file_name=file_name.get('file_name'))

    await state.clear()
