from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton, ReplyKeyboardRemove
from aiogram.utils.keyboard import InlineKeyboardBuilder

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

def delete_time(delete_time):
    choose_del = InlineKeyboardBuilder()
    [choose_del
     .add(InlineKeyboardButton(text=t, callback_data=f'd_time_{t}'))
     for t in delete_time]
    return choose_del.adjust(2).as_markup()
