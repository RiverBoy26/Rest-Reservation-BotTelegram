from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Столики'), KeyboardButton(text='Расписание')]
],
                            resize_keyboard=True,
                            input_field_placeholder="Главное меню")

tables = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Изменить')],
    [KeyboardButton(text='Вернуться назад')]
],
                            resize_keyboard=True,
                            input_field_placeholder="Столики")

schedule = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Вернуться назад')],
    [KeyboardButton(text='Выбрать время')]
],
                            resize_keyboard=True,
                            input_field_placeholder="Расписание")

time = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='8:00 - 12:00', callback_data='first_quarter_time'), 
     InlineKeyboardButton(text='12:00 - 16:00', callback_data='second_quarter_time')],
    [InlineKeyboardButton(text='16:00 - 20:00', callback_data='third_quarter_time'), 
     InlineKeyboardButton(text='20:00 - 23:00', callback_data='fourth_quarter_time')]
],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите время")

time1 = ["8:00", "9:00", "10:00", "11:00"]
time2 = ["12:00", "13:00", "14:00", "15:00"]
time3 = ["16:00", "17:00", "18:00", "19:00"]
time4 = ["20:00", "21:00", "22:00", "23:00"]

def first_time():
    tlist = InlineKeyboardBuilder()
    for t in time1:
        tlist.add(InlineKeyboardButton(text=t, callback_data=f"time_{t}"))
    return tlist.adjust(2).as_markup()

def first_time():
    tlist = InlineKeyboardBuilder()
    for t in time1:
        tlist.add(InlineKeyboardButton(text=t, callback_data=f"time_{t}"))
    return tlist.adjust(2).as_markup()

def second_time():
    tlist = InlineKeyboardBuilder()
    for t in time2:
        tlist.add(InlineKeyboardButton(text=t, callback_data=f"time_{t}"))
    return tlist.adjust(2).as_markup()

def third_time():
    tlist = InlineKeyboardBuilder()
    for t in time3:
        tlist.add(InlineKeyboardButton(text=t, callback_data=f"time_{t}"))
    return tlist.adjust(2).as_markup()

def fourth_time():
    tlist = InlineKeyboardBuilder()
    for t in time4:
        tlist.add(InlineKeyboardButton(text=t, callback_data=f"time_{t}"))
    return tlist.adjust(2).as_markup()
