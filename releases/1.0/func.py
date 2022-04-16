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

# хранение контекста
from aiogram.dispatcher import FSMContext

import sqlite3 as sql


def ExecuteSQL_getImage(img_name: str):
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


def ExecuteSQL_Image_update(img_name: str):
    """ Загружает новую картинку в БД.

    Принимает строку - имя картинки в БД.
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
            cursor_db.execute(f"UPDATE images SET img = (?) WHERE name = '{img_name}'", (image_data,) )


# Осуществляет проверку id пользователя.
# Если id = админу, то включает админку.
async def runAdmin(message: types.Message, keyboard_admin):
    """ Запуск админки.
    Осуществляет проверку id пользователя.
    Если id = админу, то переводит состояние пользователя в состояние admin
    и переключает на админ-клавиатуру."""
    admin_id_lysov = 80315171  # мой id
    admin_id_vladimir = 434967278 # id Владимира
    # user_id = message.from_user.id  # узнать id пользователя
    user_id = message.chat.id  # узнать id пользователя
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


def Print_LOG(log_text: str):
    """ Выводит лог в консоль."""
    print('LOG: ' + log_text)


async def createFormAdmin (message: types.Message, state: FSMContext) -> str:
    """Создаёт анкету админу"""
    Print_LOG("Создать анкету админу")
    allUserData = await state.get_data() # загружаем статусы пользователя
    userID = str(allUserData['userID'])
    userName = str(allUserData['userName'])
    firstName = str(allUserData['firstName'])
    lastName = str(allUserData['lastName'])
    userDanceSelect = str(allUserData['userDanceSelect'])
    userDaySelect = str(allUserData['userDaySelect'])
    userContac = str(allUserData['userContac'])
    form = ('Анкета:\n' + 
    'userID: ' + userID + '\n' + 
    'userName: ' + userName + '\n' +
    'firstName: ' + firstName + '\n' +
    'lastName: ' + lastName + '\n' +
    'userDanceSelect: ' + userDanceSelect + '\n' +
    'userDaySelect: ' + userDaySelect + '\n' +
    'userContac: ' + userContac)
    return form


async def confirmationForm (message: types.Message, state: FSMContext) -> str:
    """Подтверждение выбора пользователя и запрос контактов перед записью."""
    Print_LOG("Подтверждение выбора пользователя и запрос контактов перед записью.")
    allUserData = await state.get_data() # загружаем статусы пользователя
    # userID = str(allUserData['userID'])
    # userName = str(allUserData['userName'])
    # text = 'Оставьте Ваш номер телефона и имя. В течении суток с вами свяжется ваш тренер.'
    userDanceSelect = str(allUserData['userDanceSelect'])
    userDaySelect = str(allUserData['userDaySelect'])
    userContac = str(allUserData['userContac'])
    form = ('Вы выбрали:\n' + 
    'Танец: ' + userDanceSelect + '\n' +
    'День: ' + userDaySelect + '\n' + 
    'Контакты: ' + userContac)
    return form
