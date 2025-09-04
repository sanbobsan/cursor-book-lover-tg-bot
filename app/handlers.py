
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command, StateFilter
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app import keyboards as kb
from app import json_loader as json


router = Router()


async def answer_book(message: Message, book: dict):
    "Выводит сообщение с информацией о книге"
    text = f"""
📖 {book['title']}
👤 {book['author']}
🏷️ {book['genre']}
⭐ {round(book['mark'], 2)}
"""
    await message.answer_photo(photo=book['image_url'], caption=text, reply_markup=kb.menu)


async def answer_books(message: Message, books: list):
    "Выводит сообщение с информацией о книгах"
    text = ""
    for n, book in enumerate(books):
        text += f"{n + 1}. {book['title']} 👤 {book['author']} - {round(book['mark'], 2)}⭐\n"
    await message.answer(text=text, reply_markup=kb.menu)


class FindBook(StatesGroup):
    finding_by_genre = State()
    finding_by_title  = State()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    await message.answer('привет, я бот', reply_markup=kb.to_menu)
    await state.clear()


@router.message((F.text == "/menu") | (F.text.lower() == "меню"))
async def menu(message: Message, state: FSMContext):
    await message.answer('это меню, используй кнопки', reply_markup=kb.menu)
    await state.clear()


#region States
@router.message(F.text, FindBook.finding_by_genre)
async def find_by_genre(message: Message, state: FSMContext):
    genre = message.text.lower()
    genres = json.get_all_genres()
    if genre in [genre.lower() for genre in genres]: 
        books = json.find_books_by_genre(genre)
        await answer_books(message, books)
        await state.clear()
    else:
        await message.answer('Жанр не найден, повторите попытку', reply_markup=kb.genres)


@router.message(F.text, FindBook.finding_by_title)
async def find_by_title(message: Message, state: FSMContext):
    title = message.text.lower()
    book = json.find_book_by_title(title)
    if book is not None:
        await answer_book(message, book)
        await state.clear()
    else:
        await message.answer('Имя не найдено, повторите попытку', reply_markup=kb.to_menu)
#endregion


@router.message((F.text == "/top") | (F.text.lower() == "топ"))
async def top(message: Message):
    books = json.get_top_of_books()
    await answer_books(message, books)


@router.message((F.text == "/genre") | (F.text.lower() == "по жанрам"))
async def genre(message: Message, state: FSMContext):
    await message.answer('Выберите жанр из списка', reply_markup=kb.genres)
    await state.set_state(FindBook.finding_by_genre)


@router.message((F.text == "/random") | (F.text.lower() == "случайно"))
async def random(message: Message):
    book = json.get_random_book()
    await answer_book(message, book)


@router.message((F.text == "/search") | (F.text.lower() == "поиск"))
async def search(message: Message, state: FSMContext):
    await message.answer('Введите название книги, которую хотите найти', reply_markup=kb.to_menu)
    await state.set_state(FindBook.finding_by_title)

