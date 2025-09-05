
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app import keyboards as kb
from app import json_loader as json


router = Router()


def get_text_with_rate(book: dict):
    "Возвращает сообщение с информацией о книге и рейтинге"
    marks = ""
    for n, mark in enumerate(book["marks"]):
        stars = "⭐️" * (n + 1)
        marks += f"{stars} - {mark} оценок\n"
    
    text = f"""
📖 {book['title']}
👤 {book['author']}
🏷 {book['genre']}
⭐️ Средний рейтинг: {round(book['mark'], 2)}/8
📊 Всего оценок: {book['number_of_marks']}

📈 Распределение оценок:
{marks}
"""
    return text
    #await message.answer_photo(photo=book['image_url'], caption=text, reply_markup=kb.rate)


async def answer_book(message: Message, book: dict):
    text = get_text_with_rate(book)
    await message.answer_photo(photo=book['image_url'], caption=text, reply_markup=kb.book)


async def answer_books(message: Message, books: list, top=False):
    "Выводит сообщение с информацией о книгах"
    text = ""
    if top:
        text += "💛 Вот наш топ любимых книг ⤵️\n"
    for n, book in enumerate(books):
        text += f"{n + 1}. {book['title']} - {round(book['mark'], 2)} ⭐\n"
    await message.answer(text=text, reply_markup=kb.menu)


class FindBook(StatesGroup):
    finding_by_genre = State()
    finding_by_title  = State()
    book = State()


#region Callbacks
@router.callback_query(F.data == "delete")
async def delete(callback: CallbackQuery):
    await callback.message.delete()


@router.callback_query(F.data == "rating", FindBook.book)
async def rating(callback: CallbackQuery, state: FSMContext):
    book = (await state.get_data())["book"]
    await callback.message.edit_caption(reply_markup=kb.rate)


@router.callback_query(lambda c: c.data and c.data.startswith("rated"), FindBook.book)
async def rated(callback: CallbackQuery, state: FSMContext):
    book = (await state.get_data())["book"]
    rate = int((callback.data.split("-"))[-1])
    json.add_book_rating(book, rate)
    book = json.find_book_by_title(book["title"])
    text = get_text_with_rate(book)
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(text="Оценка добавлена!", reply_markup=kb.ok)
    await callback.message.answer_photo(photo=book["image_url"], caption=text, reply_markup=kb.menu)
#endregion


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    text = """
📖 Привет, книголюб!
✨ Я твой личный гайд по книгам!
Здесь ты найдешь топ лучших книг, можешь найти книги по жанрам и 📚названию/автору👤. 
Погружайся! Нажми кнопку меню для продолжения...
"""
    await message.answer(text=text, reply_markup=kb.to_menu)
    await state.clear()


@router.message((F.text == "/menu") | (F.text.lower() == "меню"))
async def menu(message: Message, state: FSMContext):
    text = """
✨ Здесь ты можешь погрузиться в мир книг
Ты можешь использовать комманды
/menu /top /genre /random /search
👉 Что интересует? Используй меню внизу!
"""
    await message.answer(text=text, reply_markup=kb.menu)
    await state.clear()


#region States
@router.message(F.text, FindBook.finding_by_genre)
async def find_by_genre(message: Message, state: FSMContext):
    genre = message.text
    genres = json.get_all_genres()
    if genre.lower() in [genre.lower() for genre in genres]: 
        books = json.find_books_by_genre(genre)
        await message.answer(f'🗳️ Вы выбрали "{genre}". Вот список всех книг с этим жанром ⤵️\n', reply_markup=kb.ok)
        await answer_books(message, books)
        await state.clear()
    else:
        await message.answer('Жанр не найден, повторите попытку', reply_markup=kb.genres)


@router.message(F.text, FindBook.finding_by_title)
async def find_by_title(message: Message, state: FSMContext):
    msg_text = message.text.lower()
    book = json.find_book_by_title_author(msg_text)
    if book is not None:
        await answer_book(message, book)
        await state.set_state(FindBook.book)
        await state.update_data(book=book)
    else:
        await message.answer('Имя не найдено, повторите попытку', reply_markup=kb.to_menu)
#endregion


@router.message((F.text == "/top") | (F.text.lower() == "топ"))
async def top(message: Message):
    books = json.get_top_of_books()[:10]
    await answer_books(message, books, True)


@router.message((F.text == "/genre") | (F.text.lower() == "по жанрам"))
async def genre(message: Message, state: FSMContext):
    await message.answer('Выберите жанр из списка', reply_markup=kb.genres)
    await state.set_state(FindBook.finding_by_genre)


@router.message((F.text == "/random") | (F.text.lower() == "случайно"))
async def random(message: Message, state: FSMContext):
    book = json.get_random_book()
    await answer_book(message, book)
    await state.set_state(FindBook.book)
    await state.update_data(book=book)


@router.message((F.text == "/search") | (F.text.lower() == "поиск"))
async def search(message: Message, state: FSMContext):
    await message.answer('Введите название книги, которую хотите найти', reply_markup=kb.to_menu)
    await state.set_state(FindBook.finding_by_title)

