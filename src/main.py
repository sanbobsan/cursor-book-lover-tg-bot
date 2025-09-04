from aiogram import Bot, Dispatcher
from aiogram.filters.command import Command
from aiogram.types import Message
import asyncio

# Создаём бота
token = "8445920850:AAEXH3HrLkNq1Yv2Gmfj-hjx78uDuQZCgt0"
bot = Bot(token)
# Подключаем обработчик событий
dp = Dispatcher()

@dp.message(Command('start'))
async def main(message: Message):  # Добавляем аннотацию типа
    await message.answer('Привет! Я демонстративный. Что я умею: Книги по тегам!')

# Добавляем запуск бота
async def start_bot():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(start_bot())

