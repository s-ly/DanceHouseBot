# Телеграм бот t.me/DanceHouseBot
# Школа танцев.

from re import X
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import state
import MyToken  # содержит токен

# Машина состояний
from aiogram.dispatcher.filters.state import State, StatesGroup

# хранение контекста
from aiogram.dispatcher import FSMContext 

# место для хранения контекста в ОЗУ
from aiogram.contrib.fsm_storage.memory import MemoryStorage 

# для кнопок
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup

# необходимо делать проверку на полное совпадение текста. через специальный фильтр Text 
from aiogram.dispatcher.filters import Text

# для форматирования
from aiogram.utils.markdown import italic, code

import Texts           # мой модуль, хранит текст
import func            # мой модуль, функции




# Файл MyToken.py содержит две строки:
# myToken = 'тут токен'
# testToken = 'тут токен'
# При разработке использеум test, для работы my.
# в git его игнорируем, а в место пушим зашифрованный архив.
API_TOKEN = MyToken.myToken # рабочий бот
# API_TOKEN = MyToken.testToken # тестовый бот

# Initialize bot and dispatcher
storage = MemoryStorage() # место хранения контекста в ОЗУ
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)

# создаём состояния
class StateGroupFSM(StatesGroup):
    user_state_admin = State()  # для админки
    user_state_default = State()  # все остальные

# создаём коавиатуру и добавляем кнопки
# resize_keyboard=True - уменьшает кнопки
# one_time_keyboard=True - скрыть кнопку после нажатия
# keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_about = KeyboardButton('О нас')
button_price = KeyboardButton('Прайс-лист')
button_contact = KeyboardButton('Контакты')
button_timetable = KeyboardButton('Расписание')
keyboard.add(button_about, button_price, button_contact, button_timetable)

# Клавиатура для админки
keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True)
button_exit_admin = KeyboardButton('Выход из админки')
keyboard_admin.add(button_exit_admin)




@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """ Отвечает на команду: /start когда состояние пользователя не установлено.
    Устанавливает состояние пользователя на user_state_default."""
    await StateGroupFSM.user_state_default.set()
    await message.answer(Texts.text_start, reply_markup=keyboard)    




@dp.message_handler(commands=['gs'], state='*')
async def get_state(message: types.Message, state: FSMContext):
    """ Узнать текущий статус состояния"""
    cs = await state.get_state()
    print(cs)




@dp.message_handler(Text(equals="Выход из админки"), state=StateGroupFSM.user_state_admin)
async def buttonTimetableMess(message: types.Message):
    """ Отвечает на кнопку: button_exit_admin, если состояние прльзователя admin.
    Потом переводит состояние пользователя в default."""
    await StateGroupFSM.user_state_default.set()
    await message.answer('Выход из админки', reply_markup=keyboard)




@dp.message_handler(commands=['admin'], state=StateGroupFSM.user_state_default)
async def buttonTimetableMess(message: types.Message, state: FSMContext):
    """ Отвечает на команду: /admin"""
    # await StateGroupFSM.user_state_admin.set()
    await func.runAdmin(message, keyboard_admin)




@dp.message_handler(Text(equals="Расписание"), state=StateGroupFSM.user_state_default)
async def buttonTimetableMess(message: types.Message):
    """ Отвечает на кнопку: button_timetable"""
    photo = func.getPhoto()
    await bot.send_photo(message.from_user.id, photo)





@dp.message_handler(Text(equals="О нас"), state=StateGroupFSM.user_state_default)
async def buttonAboutMess(message: types.Message):
    """ Отвечает на кнопку: utton_about"""
    # reply_markup=keyboard - показывает клавиатуру
    await message.answer(Texts.text_about, reply_markup=keyboard)




@dp.message_handler(Text(equals="Прайс-лист"), state=StateGroupFSM.user_state_default)
async def buttonPriceMess(message: types.Message):
    """ Отвечает на кнопку: utton_about"""
    # reply_markup=keyboard - показывает клавиатуру
    # code(...) и parse_mode=... форматируют текст моноширно
    await message.answer(code(Texts.text_price), parse_mode=types.ParseMode.MARKDOWN_V2, reply_markup=keyboard)




@dp.message_handler(Text(equals="Контакты"), state=StateGroupFSM.user_state_default)
async def buttonContactMess(message: types.Message):
    """ Отвечает на кнопку: utton_about"""
    # reply_markup=keyboard - показывает клавиатуру
    await message.answer(Texts.text_contact, reply_markup=keyboard)





@dp.message_handler(state=StateGroupFSM.user_state_default)
async def all_mess_state_default(message: types.Message):
    """ Отвечает на любые сообщения, если состояние не default"""
    # reply_markup=keyboard - показывает клавиатуру
    await message.answer('Используйте кнопки.', reply_markup=keyboard)




@dp.message_handler()
async def all_mess_state_default(message: types.Message):
    """ Отвечает на любые сообщения, если состояние не default"""
    await message.answer('Переброска на Start')
    await start(message)




@dp.message_handler(state=StateGroupFSM.user_state_admin)
async def allMess(message: types.Message):
    """ Отвечает на любые сообщения в админке.
    Перехватывает состояние user_state_admin."""
    await message.answer('Используйте кнопки для админки.')



if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)