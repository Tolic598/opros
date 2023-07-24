# bot/__init__.py
from aiogram import Dispatcher, Bot, types
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.middlewares import BaseMiddleware
from . import config

bot = Bot(token=config.TOKEN)
dp = Dispatcher(bot)

dp.middleware.setup(LoggingMiddleware())

# Здесь можно добавить дополнительные Middlewares, если необходимо

# Импортируем хэндлеры для регистрации
from .handlers import start, other_commands
