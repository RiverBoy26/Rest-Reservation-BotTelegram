from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

rmb = ReplyKeyboardRemove()

main = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Столики'), KeyboardButton(text='Расписание')]
],
                            resize_keyboard=True,
                            input_field_placeholder="Главное меню")

tables = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Изменить')],
    [KeyboardButton(text='Вернуться в главное меню')]
],
                            resize_keyboard=True,
                            input_field_placeholder="Столики")

go_back = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Вернуться в главное меню')]
],
                            resize_keyboard=True)

table_info = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Свободен')],
    [KeyboardButton(text='Занят')],
    [KeyboardButton(text='Забронировать')],
    [KeyboardButton(text='Вернуться в главное меню')]
],
                            resize_keyboard=True)

booking = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Забронировать')],
    [KeyboardButton(text='Удалить бронь')],
    [KeyboardButton(text='Вернуться в главное меню')]
],
                            resize_keyboard=True,
                            input_field_placeholder="Расписание")

def delete_time():
    del_t = ['12:00', '14:30', '16:50', '17:40', '18:20']
    choose_del = InlineKeyboardBuilder()
    [choose_del.add(InlineKeyboardButton(text=t, callback_data='d_time')) for t in del_t]
    return choose_del.adjust(2).as_markup()
