import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ParseMode
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Здесь необходимо указать токен вашего бота
BOT_TOKEN = "5018144842:AAHmknEVURWrdtgLXJ6d4ol9PVlYwEvLN2w"

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

# Включаем логирование
logging.basicConfig(level=logging.INFO)
dp.middleware.setup(LoggingMiddleware())


# Класс состояний опроса
class CreatePoll(StatesGroup):
    question = State()
    option1 = State()
    option2 = State()


# Обработчик команды /start
@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот для создания опросов. Введите вопрос для опроса:"
    )
    await CreatePoll.question.set()


# Обработчик вопроса от пользователя
@dp.message_handler(state=CreatePoll.question)
async def process_question(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["question"] = message.text

    await message.answer("Введите первый вариант ответа:")
    await CreatePoll.option1.set()


# Обработчик первого варианта ответа
@dp.message_handler(state=CreatePoll.option1)
async def process_option1(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["option1"] = message.text

    await message.answer("Введите второй вариант ответа:")
    await CreatePoll.option2.set()


# Обработчик второго варианта ответа и создание опроса
@dp.message_handler(state=CreatePoll.option2)
async def process_option2(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["option2"] = message.text

        # Создаем объект опроса
        poll = types.Poll(
            question=data["question"],
            options=[data["option1"], data["option2"]],
            type=types.PollType.quiz,  # Здесь можно выбрать тип опроса (quiz или regular)
            correct_option_id=0,  # Устанавливаем номер правильного варианта ответа (0 - первый вариант)
            explanation="Это объяснение правильного ответа.",
        )

        # Отправляем опрос
        await message.answer_poll(poll=poll)

    # Сбрасываем состояние FSM
    await state.finish()


if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
