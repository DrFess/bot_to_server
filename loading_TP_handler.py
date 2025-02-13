from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import Message, File

router = Router()


class LoadingHandler(StatesGroup):
    step_1 = State()


@router.message(F.text == 'Отправить отчет по травмпункту')
async def info_loading_handler(message: Message, state: FSMContext):
    await state.set_state(LoadingHandler.step_1)
    await message.answer('отправь мне файл с расширением .xslx\n '
                         'Проверь чтобы дата в название файла была полной (в формате дд.мм.гггг.)\n'
                         'Так же должно быть указано Первично или Повторно')


@router.message(LoadingHandler.step_1)
async def get_file(message: Message, state: FSMContext):
    await message.bot.download(file=message.document.file_id, destination=f'table/{message.document.file_name}')
    await state.clear()
