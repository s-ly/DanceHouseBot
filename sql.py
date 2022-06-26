###################################################################################################
# NOTE
###################################################################################################
# Работа с базой данный.
# Сейчас есть путаница, так-как методы работы с БД также есть и в модуле func.py.
# Здесь будут методы для админки, потом перенесём все методы работы с БД в этот модуль.
###################################################################################################


import sqlite3 as sql
from tkinter import image_names


def sql_read_text(key_id: int, column: str) -> str:
    """Чтение из столбца {column}, возвращает текст из таблицы."""
    SQL = f"SELECT {column} FROM texts WHERE id = {key_id}"
    with sql.connect('DanceHouseBot.db') as connect_db:
        cursor_db = connect_db.cursor()
        cursor_db.execute(SQL)
        SQL_result = cursor_db.fetchall()
    text_SQL_result = SQL_result[0][0]
    return text_SQL_result


def sql_read_img(img_name: str):
    """ Возвращает фото из БД.
    Принимает строку - имя картинки в БД."""
    SQL = f"SELECT img FROM images WHERE name = '{img_name}'"
    with sql.connect('DanceHouseBot.db') as connect_db:
        connect_db.text_factory = bytes # так-как работаем с битами
        cursor_db = connect_db.cursor()
        cursor_db.execute(SQL)
        SQL_result = cursor_db.fetchall()
    photo = SQL_result[0][0]
    return photo


def ExecuteSQL_update(key_id: int, message_text: str) -> str: 
    """Выполняет SQL запрос на запись текста в таблицу в столбец message,
    возвращает текст из таблицы.
    Использует диспетчер контекста, запросу нужно давать по очереди.
    key_id - номер строки в таблице.
    fetchall() - присваивает результат выполнения SQL запроса.
    Что бы получить результат в виде текста, делаю срез."""

    SQL_1 = f"UPDATE texts SET message = '{message_text}' WHERE id = {key_id}"
    SQL_2 = f"SELECT message FROM texts WHERE id = {key_id}"
    with sql.connect('DanceHouseBot.db') as connect_db:
        cursor_db = connect_db.cursor()
        cursor_db.execute(SQL_1)
        cursor_db.execute(SQL_2)
        SQL_result = cursor_db.fetchall()
    text_SQL_result = SQL_result[0][0]
    return text_SQL_result


def ExecuteSQL_Image_update(img_name: str, img_url_file: str = 'img.jpg'):
    """ Загружает новую картинку в БД.

    Принимает строку - имя картинки в БД.
    Принимает необязательную строку с адресом картинки на сервере.
    Фотография img.jpg находится в корне, туда её временно записываем после отправки пользователем-адмиом
    в другой функции. Здесь эту картинку считываем в объект image_data. Далее переводим данные картинки
    в специальный байт-код для SQLite. Во втором диспетчере контекста готовим и отправляем SQL-запрос.
    Компоненты BD: images - таблица, name - стоблик с названием картинок, img - столбик с картинками.
    При формировании SQL-запроса, массив байт-кода картинки передаём отдельно через (?). """

    with open(img_url_file, 'rb') as file:
        image_data = file.read()
    image_data = sql.Binary(image_data)

    with sql.connect('DanceHouseBot.db') as connect_db:
            cursor_db = connect_db.cursor()
            cursor_db.execute(f"UPDATE images SET img = (?) WHERE name = '{img_name}'", (image_data,) )