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




def getPhoto():    
    """возвращает фото расписания занятий"""
    photo = open('data/novoe_raspisanie.jpg', 'rb')
    return photo




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


