from aiogram import F, Router
from aiogram.filters import CommandStart, Command, and_f, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
from app.format_time import isTimeFormat
from datetime import datetime

router = Router()

class service(StatesGroup):
    timer = State()

class Form1(StatesGroup):
    '''Поле номера столика для редактирования'''
    table_id = State()

class Form2(StatesGroup):
    '''Поле номера столика для расписания'''
    table_id = State()

@router.message(CommandStart())
@router.message(F.text == "Вернуться в главное меню")
async def main_menu(message: Message):
    '''Главное меню'''
    await message.answer(f"Здравствуйте!\n Выберите действие.", reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    '''Сообщение со справочным материалом'''
    await message.answer('/start - начало работы!')

class status_of_tables():
    '''Изменение статуса столика'''
    @router.message(F.text == "Столики")
    async def get_tables(message: Message):
        '''Получение информации о столиках'''
        await message.answer(f'Сейчас {datetime.now().strftime("%H:%M")}\n' +
                            'Столик №1 - 3 места, стулья, у окна\n' +
                            'Столик №2 - 2 места, стулья, рядом с входом\n' +
                            'Столик №3 - 4 места, диваны и стулья, центральное расположение\n' +
                            'Столик №4 - 2 места, стулья, у окна\n' +
                            'Столик №5 - 2 места, около уборной, стулья\n' +
                            'Столик №6 - 3 места, стулья, центральная зона\n' +
                            'Столик №7 - 4 места у окна, диваны и стулья\n' +
                            'Столик №8 - 2 места, стулья, центральная зона\n' +
                            'Столик №9 - 3 места, стулья, центральная зона\n' +
                            'Столик №10 - 2 места, стулья, у окна', reply_markup=kb.tables)

    @router.message(F.text == "Изменить")
    async def table_choose1(message: Message, state: FSMContext):
        '''Выбор столика'''
        await message.answer('Выберите столик...', reply_markup=kb.go_back)
        await state.set_state(Form1.table_id)
    
    @router.message(Form1.table_id)
    async def edit_table1(message: Message, state: FSMContext):
        '''Изменение параметров столика'''
        if message.text.isdigit() and 0 < int(message.text) < 11:
            await state.update_data(table_id=message.text)
            await message.answer(f"Выберите действие для столика №{await state.get_value('table_id')}:", reply_markup=kb.table_info)
            await state.clear()
        else:
            await message.answer("Введите номер столика ещё раз!")
    
    @router.message(F.text == "Свободен")
    async def status_free(message: Message):
        await message.answer("Для столика №[в разработке] задан статус СВОБОДЕН", reply_markup=kb.go_back)
    
    @router.message(F.text == "Занят")
    async def status_busy(message: Message):
        await message.answer("Для столика №[в разработке] задан статус ЗАНЯТ", reply_markup=kb.go_back)

class schedule():
    '''Работа с расписанием конкретного столика'''
    @router.message(F.text == "Расписание")
    async def table_choose2(message: Message, state: FSMContext):
        '''Выбор столика'''
        await message.answer('Выберите столик...', reply_markup=kb.go_back)
        await state.set_state(Form2.table_id)

    @router.message(Form2.table_id)
    async def edit_table2(message: Message, state: FSMContext):
        '''Расписание столика'''
        if message.text.isdigit() and 0 < int(message.text) < 11:
            await state.update_data(table_id=message.text)
            await message.answer(f"Сейчас {datetime.now().strftime('%H:%M')}\n" +
                                 f"Расписание брони столика №{await state.get_value('table_id')}:", reply_markup=kb.booking)
            await state.clear()
        else:
            await message.answer("Введите номер столика ещё раз!")

class booking():
    '''Здесь прописаны хэндлеры для создания и удаления брони'''
    @router.message(F.text == "Забронировать")
    async def bronya_tables(message: Message, state: FSMContext):
        await message.answer("Укажите время брони!(формат: '01:24')", reply_markup=kb.go_back)
        await state.set_state(service.timer)
    
    @router.message(service.timer)
    async def create_booking(message: Message, state: FSMContext):
        if isTimeFormat(message.text):
            state.update_data(timer=message.text)
            await message.answer("Бронь создана")
            await state.clear()
        else:
            await message.answer("Некорректный формат времени. Попробуйте ещё раз!")
    
    @router.message(F.text == "Удалить бронь")
    async def del_booking(message: Message):
        await message.answer("Выберите время для удаления брони:", reply_markup=kb.go_back)
        await message.answer("Забронированные часы", reply_markup=kb.delete_time())

    @router.callback_query(F.data == 'd_time')
    async def conf_del(callback: CallbackQuery):
        await callback.answer('')
        await callback.message.edit_text('Данное время удалено!')
        await callback.message.answer(f"Сейчас {datetime.now().strftime('%H:%M')}\n" +
                                 f"Расписание брони столика №[в разработке]:", reply_markup=kb.booking)