
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

to_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню')]],
                            resize_keyboard = True,)

menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Узнать погоду')],
                            [KeyboardButton(text="Указать место")]],
                            resize_keyboard = True,)
