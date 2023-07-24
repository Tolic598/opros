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
    options = State()


# Количество опросов, которые можно создать
MAX_POLLS = 32


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

    await message.answer("Введите варианты ответов через запятую:")
    await CreatePoll.options.set()


# Обработчик опций ответов
@dp.message_handler(state=CreatePoll.options)
async def process_options(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data["options"] = [option.strip() for option in message.text.split(",")]

        if len(data["options"]) < 2:
            await message.answer("Укажите как минимум два варианта ответов.")
            return

        # Создаем объект опроса
        poll = types.Poll(
            question=data["question"],
            options=data["options"],
            type=types.PollType.QUIZ,  # Здесь можно выбрать тип опроса (QUIZ или REGULAR)
            correct_option_id=0,  # Устанавливаем номер правильного варианта ответа (0 - первый вариант)
            explanation="Это объяснение правильного ответа.",
        )

        # Отправляем опрос
        await message.bot.send_poll(
            chat_id=message.chat.id,
            question=poll.question,
            options=poll.options,
            type=poll.type,
            correct_option_id=poll.correct_option_id,
            explanation=poll.explanation,
        )

    # Сбрасываем состояние FSM
    await state.finish()


if __name__ == "__main__":
    from aiogram import executor

    executor.start_polling(dp, skip_updates=True)
