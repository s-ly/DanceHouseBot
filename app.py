# Телеграм бот t.me/DanceHouseBot
# Школа танцев.

from aiogram import Bot, Dispatcher, executor, types
import MyToken  # содержит токен

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
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

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




@dp.message_handler(Text(equals="Расписание"))
async def buttonTimetableMess(message: types.Message):
    """ Отвечает на кнопку: button_timetable"""
    photo = func.getPhoto()
    await bot.send_photo(message.from_user.id, photo)





@dp.message_handler(Text(equals="О нас"))
async def buttonAboutMess(message: types.Message):
    """ Отвечает на кнопку: utton_about"""
    # reply_markup=keyboard - показывает клавиатуру
    await message.answer(Texts.text_about, reply_markup=keyboard)




@dp.message_handler(Text(equals="Прайс-лист"))
async def buttonPriceMess(message: types.Message):
    """ Отвечает на кнопку: utton_about"""
    # reply_markup=keyboard - показывает клавиатуру
    # code(...) и parse_mode=... форматируют текст моноширно

    await message.answer(code(Texts.text_price), parse_mode=types.ParseMode.MARKDOWN_V2, reply_markup=keyboard)




@dp.message_handler(Text(equals="Контакты"))
async def buttonContactMess(message: types.Message):
    """ Отвечает на кнопку: utton_about"""
    # reply_markup=keyboard - показывает клавиатуру
    await message.answer(Texts.text_contact, reply_markup=keyboard)




@dp.message_handler()
async def allMess(message: types.Message):
    """ Отвечает на любые сообщения."""
    # reply_markup=keyboard - показывает клавиатуру
    await message.answer('Используйте кнопки.', reply_markup=keyboard)




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)