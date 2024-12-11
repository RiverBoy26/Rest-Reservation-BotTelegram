from aiogram import F, Router
from aiogram.filters import CommandStart, Command, and_f, or_f
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

import app.keyboards as kb
import app.database.requests as rq
from app.format_time import isTimeFormat
from datetime import datetime

router = Router()

class service(StatesGroup):
    timer = State()

class add(StatesGroup):
    '''Поле номера столика для его добавления'''
    info_of_table = State()

class delete(StatesGroup):
    '''Поле номера столика для его удаления'''
    table_number = State()

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
    await rq.set_user(message.from_user.id)
    await message.answer(f"Здравствуйте!\nВыберите действие.", reply_markup=kb.main)

@router.message(Command('help'))
async def get_help(message: Message):
    '''Сообщение со справочным материалом'''
    await message.answer('/start - начало работы!\n/add - добавление столика\n/delete - удаление столика')
class t_add():
    '''Процесс добавления столика'''
    @router.message(Command('add'))
    async def add_table(message: Message, state: FSMContext):
        '''Добавление столика'''
        await message.answer('Введите номер столика, кол-во мест и его описание в формате "[№столика] [кол-во мест] [описание]".\nПример ввода: "1 2 window"', reply_markup=kb.rmb)
        await state.set_state(add.info_of_table)
    
    @router.message(add.info_of_table)
    async def edit_add(message: Message, state: FSMContext):
        '''Проверка введённой информации и добавление в бд'''
        info = [message for message in str(message.text).split()]
        description = ' '.join(info[2:])
        all_tables = await rq.get_tables()
        list_num_tables = [t.table_number for t in all_tables]
        if (info[0].isdigit() and int(info[0]) > 0 and int(info[0]) not in list_num_tables) and (info[1].isdigit() and int(info[1]) > 0) and len(description) <= 255:
            await rq.set_table(info[0], info[1], description)
            await state.update_data(info_of_table=message.text)
            await message.answer('Столик успешно добавлен!')
            await state.clear()
        else:
            await message.answer('Некорректный ввод информации! Попробуйте ещё раз!')

class t_delete():
    @router.message(Command('delete'))
    async def del_table(message: Message, state: FSMContext):
        '''Удаление столика'''
        await message.answer('Введите номер столика, который хотите удалить.', reply_markup=kb.rmb)
        await state.set_state(delete.table_number)
    
    @router.message(delete.table_number)
    async def edit_del(message: Message, state: FSMContext):
        num = message.text
        all_tables = await rq.get_tables()
        list_num_tables = [t.table_number for t in all_tables]
        if num.isdigit() and int(num) in list_num_tables:
            await rq.delete_table(num)
            await state.update_data(table_number=message.text)
            await message.answer('Столик успешно удалён!')
            await state.clear()
        else:
            await message.answer('Этого столика не существует! Попробуйте ещё раз!')

class status_of_tables():
    '''Изменение статуса столика'''
    @router.message(F.text == "Столики")
    async def get_tables(message: Message):
        '''Получение информации о столиках'''
        all_tables = await rq.get_tables()
        tbl_info = "".join([f"Столик №{t.table_number}: кол-во мест - {t.number_of_seats}, {t.description} - {'Занят❌' if await rq.get_is_occupied_now(t.id) else 'Свободен✅'}\n" for t in all_tables])
        await message.answer(f'Сейчас {datetime.now().strftime("%H:%M")}\n' + tbl_info, reply_markup=kb.tables)

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
