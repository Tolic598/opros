# main.py
from aiogram import Bot, Dispatcher, types
from aiogram import start_polling
from .bot import dp

def main():
    from . import handlers  # Импортируем хэндлеры, чтобы они были зарегистрированы

    start_polling(dp, skip_updates=True)

if __name__ == '__main__':
    main()
