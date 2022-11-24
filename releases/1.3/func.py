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


# Осуществляет проверку id пользователя.
# Если id = админу, то включает админку.
async def runAdmin(message: types.Message, keyboard_admin):
    """ Запуск админки.
    Осуществляет проверку id пользователя.
    Если id = админу, то переводит состояние пользователя в состояние admin
    и переключает на админ-клавиатуру."""
    admin_id_lysov = 80315171  # мой id
    admin_id_vladimir = 434967278 # id Владимира
    admin_id_linda = 1170918217 # id Линды
    # user_id = message.from_user.id  # узнать id пользователя
    user_id = message.chat.id  # узнать id пользователя
    print(user_id)
    if (user_id == admin_id_lysov or user_id == admin_id_vladimir or user_id == admin_id_linda):
        await StateGroupFSM.user_state_admin.set()
        await message.answer('Вход в админку', reply_markup=keyboard_admin)
    else:
        await message.answer('Только для админов')



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
