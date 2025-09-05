
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder

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


book = InlineKeyboardBuilder()
book.row(InlineKeyboardButton(
    text="Оценить", callback_data="rating"))
book = book.as_markup()


rate = InlineKeyboardBuilder()
for i in range(1, 9):
    rate.add(InlineKeyboardButton(text=f"{str(i)} ⭐",
                        callback_data="rated"))
rate.adjust(4)
rate = rate.as_markup()


ok = InlineKeyboardBuilder()
ok.button(text="Ок", callback_data="delete")
ok = ok.as_markup()
