from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.database.requests import get_tables_with_status

router = Router()

class Form(StatesGroup):
    '''Поле номера столика для редактирования'''
    table_id = State()

@router.message(CommandStart())
async def main_menu(message: Message):
    '''Главное меню'''
    await message.answer(f"Здравствуйте!\nВыберите действие.", reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    '''Сообщение со справочным материалом'''
    await message.answer('/start - начало работы!')


@router.message(F.text == "Столики")
async def get_tables(message: Message):
    '''Получение информации о столиках'''
    tables = await get_tables_with_status()

    if not tables:
        await message.answer("Нет доступных столиков.")
        return

    tables_info = "\n".join([
        f"Столик №{table['id']}: {table['description']} - {table['status']}"
        for table in tables
    ])
    await message.answer(f"Список столиков:\n\n{tables_info}", reply_markup=kb.tables)

@router.message(F.text == "Изменить")
async def table_choose(message: Message, state: FSMContext):
    '''Выбор столика'''
    await message.answer('Выберите столик...', reply_markup=kb.go_back)
    await state.set_state(Form.table_id)

@router.message(Form.table_id)
async def edit_table(message: Message, state: FSMContext):
    '''Изменение параметров столика'''
    await state.update_data(table_id=message.text)
    await message.answer(f"Выберите действие для столика №{await state.get_value('table_id')}:", reply_markup=kb.table_info)
    await state.clear()



@router.message(F.text == "Расписание")
async def get_schedule(message: Message):
    '''Выбор действия с расписанием'''
    await message.answer('Выберите действие для расписания:', reply_markup=kb.schedule)

#Выбор времени
@router.message(F.text == "Выбрать время")
async def get_time(message: Message):
    '''Выбор времени'''
    await message.answer('Выберите время:', reply_markup=kb.time)

@router.callback_query(F.data == 'first_quarter_time')
async def first_quarter_time(callback: CallbackQuery):
    await callback.answer('')
    await callback.message.edit_text('Выберите точное время:', reply_markup=kb.first_time())

@router.callback_query(F.data == 'second_quarter_time')
async def second_quarter_time(callback: CallbackQuery):
    await callback.answer('2')
    await callback.message.edit_text('Выберите точное время:', reply_markup=kb.second_time())

@router.callback_query(F.data == 'third_quarter_time')
async def third_quarter_time(callback: CallbackQuery):
    await callback.answer('3')
    await callback.message.edit_text('Выберите точное время:', reply_markup=kb.third_time())

@router.callback_query(F.data == 'fourth_quarter_time')
async def fourth_quarter_time(callback: CallbackQuery):
    await callback.answer('4')
    await callback.message.edit_text('Выберите точное время:', reply_markup=kb.fourth_time())

@router.message(F.text == "Вернуться назад")
async def go_start(message: Message):
    message.reply("Кнопка в разработке")


@router.callback_query(F.data == "time")
async def print_time(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.reply(text="Одинаковый текст для всех столиков")