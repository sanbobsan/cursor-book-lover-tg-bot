
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder

from app.json_loader import get_all_genres

to_menu = ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text='Меню')]],
                            resize_keyboard = True,)


menu = ReplyKeyboardMarkup(keyboard=[
    [KeyboardButton(text='Топ'), KeyboardButton(text='По жанрам'), KeyboardButton(text='Случайно')],
    [KeyboardButton(text='Поиск')]], 
                            resize_keyboard = True,)



genres = ReplyKeyboardBuilder()
for genre in get_all_genres():
    genres.add(KeyboardButton(text=str(genre)))
genres.adjust(6)
genres = genres.as_markup(resize_keyboard=True)
