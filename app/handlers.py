
from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext

from app import keyboards as kb


router = Router()


class Enter_location(StatesGroup):
    location = State()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer('привет, ты нажал кмд старт', reply_markup=kb.to_menu)


@router.message(F.text.lower() == 'меню')
async def menu(message: Message, state: FSMContext):
    await message.answer('Это меню, выберите что хотите)', reply_markup=kb.menu)
    await state.clear()

