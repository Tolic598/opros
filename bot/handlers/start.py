# bot/handlers/start.py
from aiogram import types
from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from .. import dp

class MyStates(StatesGroup):
    state1 = State()
    state2 = State()
    # Добавьте здесь необходимые состояния для вашего бота

@dp.message_handler(Command("start"))
async def cmd_start(message: types.Message):
    # Здесь вы можете добавить логику, связанную с обработкой команды /start
    await message.answer("Привет! Я бот на Aiogram с MySQL.")
