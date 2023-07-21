import logging
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import Poll, PollType

# Вставьте сюда ваш токен
TOKEN = "5556147625:AAGuKsc7MqGGodi2vScq7Wp7C2ssXZm1gsA"

# Инициализация бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(LoggingMiddleware())

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Привет! Я бот для создания опросов. Введите ваши варианты через запятую:")

# Обработчик текстового сообщения с вариантами опроса
@dp.message_handler(lambda message: message.text.count(',') >= 31)
async def create_poll(message: types.Message):
    # Разбиваем варианты опроса на отдельные элементы
    options = message.text.split(',')
    options = [option.strip() for option in options]

    # Проверяем, что количество вариантов не превышает 32 (максимум для опросов в Telegram)
    if len(options) <= 32:
        poll = Poll(
            type=PollType.QUIZ,
            question="Выберите один из вариантов:",
            options=options,
            correct_option_id=0  # Номер правильного варианта (в данном случае - первый)
        )
        await bot.send_poll(chat_id=message.chat.id, poll=poll, disable_notification=True)
    else:
        await message.reply("Извините, максимальное количество вариантов для опроса - 32.")

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    # Запуск бота
    from aiogram import executor
    executor.start_polling(dp, skip_updates=True)
