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

time1 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='8:00 - 12:00', callback_data='first_quarter_time'), 
     InlineKeyboardButton(text='12:00 - 16:00', callback_data='second_quarter_time')],
    [InlineKeyboardButton(text='16:00 - 20:00', callback_data='third_quarter_time'), 
     InlineKeyboardButton(text='20:00 - 23:00', callback_data='fourth_quarter_time')]
],
                            resize_keyboard=True,
                            input_field_placeholder="Выберите время")

time2 = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='1', callback_data=''),
     InlineKeyboardButton(text='2', callback_data='')],
    [InlineKeyboardButton(text='3', callback_data=''), 
     InlineKeyboardButton(text='4', callback_data='')]
],                           
                            resize_keyboard=True,
                            input_field_placeholder="dsds")