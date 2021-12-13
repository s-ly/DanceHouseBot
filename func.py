# Фукции для бота
# from aiogram.dispatcher.filters import state

from aiogram import Bot, Dispatcher, executor, types

# Машина состояний
# from aiogram.dispatcher.filters.state import State, StatesGroup

# хранение контекста
# from aiogram.dispatcher import FSMContext 

# место для хранения контекста в ОЗУ
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# Мой класс для работы с состояниями пользователя
from app import StateGroupFSM 

import sqlite3 as sql




def ExecuteSQL_getImage():
    """возвращает фото расписания занятий из базы данных."""
    SQL = "SELECT img FROM images WHERE name = 'timetable'"
    with sql.connect('DanceHouseBot.db') as connect_db:
        connect_db.text_factory = bytes # так-как работаем с битами
        cursor_db = connect_db.cursor()
        cursor_db.execute(SQL)
        SQL_result = cursor_db.fetchall()
    photo = SQL_result[0][0]
    return photo




def ExecuteSQL_Image_update():
    """ Загружает новую картинку расписания в БД.
    Фотография img.jpg находится в корне, туда её временно записываем после отправки пользователем-адмиом
    в другой функции. Здесь эту картинку считываем в объект image_data. Далее переводим данные картинки
    в специальный байт-код для SQLite. Во втором диспетчере контекста готовим и отправляем SQL-запрос.
    Компоненты BD: images - таблица, name - стоблик с названием картинок, img - столбик с картинками.
    При формировании SQL-запроса, массив байт-кода картинки передаём отдельно через (?). """

    with open('img.jpg', 'rb') as file:
        image_data = file.read()
    image_data = sql.Binary(image_data)

    with sql.connect('DanceHouseBot.db') as connect_db:
            cursor_db = connect_db.cursor()
            cursor_db.execute("UPDATE images SET img = (?) WHERE name = 'timetable'", (image_data,) )




# Осуществляет проверку id пользователя.
# Если id = админу, то включает админку.
async def runAdmin(message: types.Message, keyboard_admin):
    """ Запуск админки.
    Осуществляет проверку id пользователя.
    Если id = админу, то переводит состояние пользователя в состояние admin
    и переключает на админ-клавиатуру."""
    admin_id_lysov = 80315171  # мой id
    admin_id_vladimir = 434967278 # id Владимира
    user_id = message.from_user.id  # узнать id пользователя
    print(user_id)
    if (user_id == admin_id_lysov or user_id == admin_id_vladimir):
        await StateGroupFSM.user_state_admin.set()
        await message.answer('Вход в админку', reply_markup=keyboard_admin)
    else:
        await message.answer('Только для админов')




def ExecuteSQL(key_id: int) -> str:
    """Выполняет SQL запрос на чтение из столбца message, возвращает текст из таблицы."""
    SQL = f"SELECT message FROM texts WHERE id = {key_id}"
    with sql.connect('DanceHouseBot.db') as connect_db:
        cursor_db = connect_db.cursor()
        cursor_db.execute(SQL)
        SQL_result = cursor_db.fetchall()
    text_SQL_result = SQL_result[0][0]
    return text_SQL_result




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


