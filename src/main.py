# # from aiogram import Bot, Dispatcher
# # from aiogram.filters.command import Command
# # from aiogram.types import Message
# # import asyncio
# #
# # # Создаём бота
# # token = "8445920850:AAEXH3HrLkNq1Yv2Gmfj-hjx78uDuQZCgt0"
# # bot = Bot(token)
# # # Подключаем обработчик событий
# # dp = Dispatcher()
# #
# # @dp.message(Command('start'))
# # async def main(message: Message):  # Добавляем аннотацию типа
# #     await message.answer('Привет! Я демонстративный. Что я умею: Книги по тегам!')
# #
# # # Добавляем запуск бота
# # async def start_bot():
# #     await dp.start_polling(bot)
# #
# # if __name__ == "__main__":
# #     asyncio.run(start_bot())
#
# import os
# import asyncio
# from aiogram import Bot, Dispatcher, types, F
# from aiogram.filters import Command
# from aiogram.fsm.context import FSMContext
# from aiogram.fsm.state import State, StatesGroup
# from aiogram.types import Message, ReplyKeyboardRemove
# from aiogram.utils.keyboard import InlineKeyboardBuilder
#
# # Mock data
# books = [
#     {
#         "title": "Война и мир",
#         "author": "Лев Толстой",
#         "genre": "Роман",
#         "image_url": "https://static.insales-cdn.com/images/products/1/160/208213088/large_%D0%92%D0%BE%D0%B9%D0%BD%D0%B0_%D0%B8_%D0%BC%D0%B8%D1%80_%D0%9B.%D0%9D._%D0%A2%D0%BE%D0%BB%D1%81%D1%82%D0%BE%D0%B9.jpg",
#         "reviews": ["Великая книга", "Классика", "Много персонажей"]
#     },
#     {
#         "title": "Преступление и наказание",
#         "author": "Федор Достоевский",
#         "genre": "Роман",
#         "image_url": "https://cdn.img-gorod.ru/nomenclature/27/000/27000053.jpg",
#         "reviews": ["Глубокое произведение", "Психологический роман"]
#     },
#     {
#         "title": "Мастер и Маргарита",
#         "author": "Михаил Булгаков",
#         "genre": "Роман",
#         "image_url": "https://cdn.img-gorod.ru/nomenclature/22/000/22000060.jpg",
#         "reviews": ["Мистика", "Любовь и творчество"]
#     },
#     {
#         "title": "1984",
#         "author": "Джордж Оруэлл",
#         "genre": "Антиутопия",
#         "image_url": "https://upload.wikimedia.org/wikipedia/ru/c/c0/1984_first_edition_cover.jpg",
#         "reviews": ["Тоталитаризм", "Пророчество"]
#     }
# ]
#
# class SearchState(StatesGroup):
#     waiting_for_query = State()
#
# # Токен бота
# token = "8445920850:AAEXH3HrLkNq1Yv2Gmfj-hjx78uDuQZCgt0"
# bot = Bot(token)
# dp = Dispatcher()
#
# @dp.message(Command('start'))
# async def cmd_start(message: Message):
#     await message.answer(
#         "Привет! Я бот для поиска книг.\n"
#         "Используй команду /search для поиска книг по названию или автору."
#     )
#
# @dp.message(Command('search'))
# async def cmd_search(message: Message, state: FSMContext):
#     await message.answer("Введите название книги или автора для поиска:")
#     await state.set_state(SearchState.waiting_for_query)
#
# @dp.message(SearchState.waiting_for_query)
# async def process_search(message: Message, state: FSMContext):
#     query = message.text.lower()
#     found_books = []
#     for book in books:
#         if query in book['title'].lower() or query in book['author'].lower():
#             found_books.append(book)
#
#     if not found_books:
#         await message.answer("Книги по вашему запросу не найдены.")
#         await state.clear()
#         return
#
#     # Ограничим вывод тремя книгами
#     for book in found_books[:3]:
#         # Формируем текст с информацией о книге
#         text = f"Название: {book['title']}\nАвтор: {book['author']}\nЖанр: {book['genre']}\n"
#         if book['reviews']:
#             text += "Отзывы:\n" + "\n".join([f"- {review}" for review in book['reviews']])
#         else:
#             text += "Отзывов пока нет."
#
#         # Отправляем картинку и текст
#         await message.answer_photo(photo=book['image_url'], caption=text)
#
#     await state.clear()
#
# if __name__ == '__main__':
#     asyncio.run(dp.start_polling(bot))


import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest

# Mock data с проверенными URL изображений
books = [
    {
        "title": "Война и мир",
        "author": "Лев Толстой",
        "genre": "Роман",
        "image_url": "https://via.placeholder.com/300x400?text=Война+и+мир",
        "reviews": ["Великая книга", "Классика", "Много персонажей"]
    },
    {
        "title": "Преступление и наказание",
        "author": "Федор Достоевский",
        "genre": "Роман",
        "image_url": "https://via.placeholder.com/300x400?text=Преступление+и+наказание",
        "reviews": ["Глубокое произведение", "Психологический роман"]
    },
    {
        "title": "Мастер и Маргарита",
        "author": "Михаил Булгаков",
        "genre": "Роман",
        "image_url": "https://via.placeholder.com/300x400?text=Мастер+и+Маргарита",
        "reviews": ["Мистика", "Любовь и творчество"]
    },
    {
        "title": "1984",
        "author": "Джордж Оруэлл",
        "genre": "Антиутопия",
        "image_url": "https://via.placeholder.com/300x400?text=1984",
        "reviews": ["Тоталитаризм", "Пророчество"]
    }
]

class SearchState(StatesGroup):
    waiting_for_query = State()

# Токен бота
token = "8445920850:AAEXH3HrLkNq1Yv2Gmfj-hjx78uDuQZCgt0"
bot = Bot(token)
dp = Dispatcher()

@dp.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer(
        "Привет! Я бот для поиска книг.\n"
        "Используй команду /search для поиска книг по названию или автору.\n\n"
        "Также доступны команды:\n"
        "/top - топ книг\n"
        "/random - случайная книга"
    )

@dp.message(Command('search'))
async def cmd_search(message: Message, state: FSMContext):
    await message.answer("Введите название книги или автора для поиска:")
    await state.set_state(SearchState.waiting_for_query)

@dp.message(Command('top'))
async def cmd_top(message: Message):
    # Показываем топ-3 книги
    top_books = books[:3]
    for book in top_books:
        text = f"📖 {book['title']}\n👤 {book['author']}\n🏷️ {book['genre']}\n"
        if book['reviews']:
            text += "⭐ Отзывы:\n" + "\n".join([f"- {review}" for review in book['reviews'][:2]])

        try:
            await message.answer_photo(photo=book['image_url'], caption=text)
        except TelegramBadRequest:
            # Если не удалось отправить фото, отправляем только текст
            await message.answer(text)

@dp.message(Command('random'))
async def cmd_random(message: Message):
    import random
    book = random.choice(books)
    text = f"📖 {book['title']}\n👤 {book['author']}\n🏷️ {book['genre']}\n"
    if book['reviews']:
        text += "⭐ Отзывы:\n" + "\n".join([f"- {review}" for review in book['reviews'][:2]])

    try:
        await message.answer_photo(photo=book['image_url'], caption=text)
    except TelegramBadRequest:
        await message.answer(text)

@dp.message(SearchState.waiting_for_query)
async def process_search(message: Message, state: FSMContext):
    query = message.text.lower()
    found_books = []

    for book in books:
        if query in book['title'].lower() or query in book['author'].lower():
            found_books.append(book)

    if not found_books:
        await message.answer("Книги по вашему запросу не найдены.")
        await state.clear()
        return

    for book in found_books[:3]:
        text = f"📖 {book['title']}\n👤 {book['author']}\n🏷️ {book['genre']}\n"
        if book['reviews']:
            text += "⭐ Отзывы:\n" + "\n".join([f"- {review}" for review in book['reviews'][:2]])

        try:
            await message.answer_photo(photo=book['image_url'], caption=text)
        except TelegramBadRequest:
            # Если не удалось отправить фото, отправляем только текст
            await message.answer(text)

    await state.clear()

if __name__ == '__main__':
    asyncio.run(dp.start_polling(bot))