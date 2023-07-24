import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor

# Установите ваш токен Telegram бота
BOT_TOKEN = '5018144842:AAHmknEVURWrdtgLXJ6d4ol9PVlYwEvLN2w'

logging.basicConfig(level=logging.INFO)

# Инициализация бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)


# Обработчик команды /create_poll
@dp.message_handler(commands=['create_poll'])
async def create_poll(message: types.Message):
    # Вопрос для опроса
    question = "Выберите ваш любимый вариант:"
    # Варианты ответов для опроса
    options = [
        "Вариант 1", "Вариант 2", "Вариант 3", "Вариант 4", "Вариант 5",
        "Вариант 6", "Вариант 7", "Вариант 8", "Вариант 9", "Вариант 10",
        "Вариант 11", "Вариант 12", "Вариант 13", "Вариант 14", "Вариант 15",
        "Вариант 16", "Вариант 17", "Вариант 18", "Вариант 19", "Вариант 20",
        "Вариант 21", "Вариант 22", "Вариант 23", "Вариант 24", "Вариант 25",
        "Вариант 26", "Вариант 27", "Вариант 28", "Вариант 29", "Вариант 30",
        "Вариант 31", "Вариант 32",
    ]

    # Создаем объект опроса
    poll = types.Poll(
        question=question,
        options=options,
        type=types.PollType.QUIZ,
        correct_option_id=0  # Номер варианта, который считается верным (начиная с 0)
    )

    # Отправляем опрос пользователю
    try:
        sent_poll = await bot.send_poll(chat_id=message.chat.id, question=poll.question, options=poll.options,
                                        type=poll.type, correct_option_id=poll.correct_option_id, is_anonymous=False)
        logging.info(f"Опрос создан с ID: {sent_poll.poll.id}")
    except Exception as e:
        logging.error(f"Ошибка при создании опроса: {e}")
        await message.answer("Произошла ошибка при создании опроса. Пожалуйста, попробуйте позже.")


# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    await message.reply("Привет! Я бот для создания опросов. Используйте команду /create_poll, чтобы создать опрос.")


# Обработчик неизвестных команд
@dp.message_handler()
async def unknown_command(message: types.Message):
    await message.reply("Извините, я не понимаю данную команду. Попробуйте другую или используйте /create_poll.")


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, loop=loop, skip_updates=True)
