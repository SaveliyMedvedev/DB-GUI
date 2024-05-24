import mysql.connector
from mysql.connector import Error

from conf import HOST, USER, PASSWORD, DATABASE_NAME


def connection_decorator(func):
    def wrapper(*args, **kwargs):
        try:
            connection = mysql.connector.connect(
                host=HOST,
                user=USER,
                password=PASSWORD,
                database=DATABASE_NAME,
            )
            if connection.is_connected():
                return func(connection, *args, **kwargs)
        except Error as e:
            print(f"Ошибка подключения к базе данных: {e}")
        finally:
            if connection.is_connected():
                connection.close()
    return wrapper
