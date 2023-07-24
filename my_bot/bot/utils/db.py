# utils/db.py
import mysql.connector
from mysql.connector import Error
from .. import config

def connect():
    try:
        connection = mysql.connector.connect(
            host=config.DB_HOST,
            user=config.DB_USER,
            password=config.DB_PASSWORD,
            database=config.DB_DATABASE
        )
        return connection
    except Error as e:
        print("Ошибка при подключении к MySQL:", e)
        return None
