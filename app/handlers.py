from aiogram import F, Router
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery

import app.keyboards as kb

router = Router()

@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('Привет!', reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    await message.answer('/start - начало работы!')

@router.message(F.text == "Столики")
async def get_tables(message: Message):
    await message.answer('текст про столы', reply_markup=kb.tables)

@router.message(F.text == "Расписание")
async def get_schedule(message: Message):
    await message.answer('Выберите действие для расписания:', reply_markup=kb.schedule)

#Выбор времени
@router.message(F.text == "Выбрать время")
async def get_time1(message: Message):
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
    await callback.answer('penis')
    await callback.message.edit_text('Выберите точное время:', reply_markup=kb.fourth_time())

@router.message(F.text == "Вернуться назад")
async def go_start(message: Message):
    await message.answer("/start")


@router.callback_query(F.data == "time")
async def print_time(callback: CallbackQuery):
    await callback.answer("")
    await callback.message.answer(text="Одинаковый текст для всех столиков")