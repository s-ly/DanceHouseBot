# Телеграм бот t.me/DanceHouseBot
# Школа танцев.

from re import X
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters import state
# from aiogram.types import inline_keyboard
# from aiogram.types import reply_keyboard
# from aiogram.types.callback_query import CallbackQuery
# from aiogram.types import CallbackQuery
import MyToken  # содержит токен

# Машина состояний
from aiogram.dispatcher.filters.state import State, StatesGroup

# хранение контекста
from aiogram.dispatcher import FSMContext 

# место для хранения контекста в ОЗУ
from aiogram.contrib.fsm_storage.memory import MemoryStorage 

# для кнопок
from aiogram.types.reply_keyboard import KeyboardButton, ReplyKeyboardMarkup

# для Инлайн-клавиатуры
# from aiogram.types.inline_keyboard import InlineKeyboardButton, InlineKeyboardMarkup

# необходимо делать проверку на полное совпадение текста. через специальный фильтр Text 
from aiogram.dispatcher.filters import Text

# для форматирования
from aiogram.utils.markdown import italic, code, text

# import Texts           # мой модуль, хранит текст
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
    user_state_admin_edit_about = State()  # для админки, жду ввод текста 'О нас'
    user_state_admin_edit_price = State()  # для админки, жду ввод текста 'Прайс-лист'
    user_state_admin_edit_contact = State()  # для админки, жду ввод текста 'Контакты'
    user_state_admin_edit_image = State()  # админка, жду картинку 'Расписание'
    user_state_admin_edit_poster = State()  # админка, жду картинку 'Афиша'

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
button_poster = KeyboardButton('Афиша')
keyboard.add(button_about, button_price, button_contact, button_timetable, button_poster)

# Клавиатура для админки
keyboard_admin = ReplyKeyboardMarkup(resize_keyboard=True)
button_exit_admin = KeyboardButton('Выход из админки')
button_show_about = KeyboardButton('Показ: О нас')
button_show_price = KeyboardButton('Показ: Прайс-лист')
button_show_contact = KeyboardButton('Показ: Контакты')
button_show_image = KeyboardButton('Показ: Расписание')
button_show_poster = KeyboardButton('Показ: Афиша')
button_edit_about = KeyboardButton('Ред: О нас')
button_edit_price = KeyboardButton('Ред: Прайс-лист')
button_edit_contact = KeyboardButton('Ред: Контакты')
button_edit_image = KeyboardButton('Ред: Расписание')
button_edit_poster = KeyboardButton('Ред: Афиша')
keyboard_admin.add(button_show_about, button_edit_about,
button_show_price, button_edit_price,
button_show_contact, button_edit_contact,
button_exit_admin, button_show_image, button_edit_image,
button_show_poster, button_edit_poster)

# Инлайн-клавиатура
inline_key_contacts = types.InlineKeyboardMarkup() 
inline_but_web = types.InlineKeyboardButton(
    text='Записаться на пробное занятие',
    url='https://kazandanceschool.ru/')
inline_key_contacts.add(inline_but_web)
# inline_keyboard_test = types.InlineKeyboardMarkup()
# inline_button_test = types.InlineKeyboardButton(text='1', callback_data='1')
# inline_button_test2 = types.InlineKeyboardButton(text='2', url='https://vk.com/s.lysov')
# inline_keyboard_test.add(inline_button_test, inline_button_test2)


# @dp.callback_query_handler(text='1', state='*')
# async def process_callback_button1(call_inline: types.CallbackQuery):
#     """ Обработка inline-кнопки. 
#     call_inline.answer(...) - выводит окошко с надписью, что бы откллчить таймер кнопки,
#     но можно просто - await call_inline.answer()."""
#     print("Обработка inline-кнопки")
#     await call_inline.answer()


@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    """ Отвечает на команду: /start когда состояние пользователя не установлено.
    Устанавливает состояние пользователя на user_state_default."""
    await StateGroupFSM.user_state_default.set()
    await message.answer(func.ExecuteSQL(4), reply_markup=keyboard) 


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


###################################################################################################
# Показ данных
###################################################################################################
@dp.message_handler(Text(equals="Показ: Афиша"), state=StateGroupFSM.user_state_admin)
@dp.message_handler(Text(equals="Афиша"), state=StateGroupFSM.user_state_default)
async def buttonTimetableMess(message: types.Message):
    """ Показывает Афишу. """
    print('кнопка афиша')
    photo = func.ExecuteSQL_getImage('poster')
    await bot.send_photo(message.from_user.id, photo)


@dp.message_handler(Text(equals="Показ: Расписание"), state=StateGroupFSM.user_state_admin)
@dp.message_handler(Text(equals="Расписание"), state=StateGroupFSM.user_state_default)
async def buttonTimetableMess(message: types.Message):
    """ Показывает расписание. """
    photo = func.ExecuteSQL_getImage('timetable')
    await bot.send_photo(message.from_user.id, photo)


@dp.message_handler(Text(equals="Показ: О нас"), state=StateGroupFSM.user_state_admin)
@dp.message_handler(Text(equals="О нас"), state=StateGroupFSM.user_state_default)
async def buttonAboutMess(message: types.Message):
    """ Показывает О нас. """
    await message.answer(func.ExecuteSQL(1))


@dp.message_handler(Text(equals="Показ: Прайс-лист"), state=StateGroupFSM.user_state_admin)
@dp.message_handler(Text(equals="Прайс-лист"), state=StateGroupFSM.user_state_default)
async def buttonPriceMess(message: types.Message):
    """ Показывает Прайс-лист.
    # code(...) и parse_mode=... форматируют текст моноширно. """
    await message.answer(code(func.ExecuteSQL(2)), parse_mode=types.ParseMode.MARKDOWN_V2)


@dp.message_handler(Text(equals="Показ: Контакты"), state=StateGroupFSM.user_state_admin)
@dp.message_handler(Text(equals="Контакты"), state=StateGroupFSM.user_state_default)
async def buttonContactMess(message: types.Message):
    """ Показывает Контакты.
    Дополнительно показывает инлайн-клавиатуру."""
    await message.answer(func.ExecuteSQL(3), reply_markup=inline_key_contacts)
    print('кнопка отправленна')


###################################################################################################
# Редактирование в админке
###################################################################################################
@dp.message_handler(Text(equals="Ред: О нас"), state=StateGroupFSM.user_state_admin)
async def buttonContactMess(message: types.Message):
    """ Отвечает на кнопку 'Ред: О нас'. 
    Переводит пользователя администратора в состояние:
    жду ввод текста 'О нас'. """
    await message.answer('Редактирование пункта: О нас. Введите новый текст.')
    await StateGroupFSM.user_state_admin_edit_about.set()


@dp.message_handler(Text(equals="Ред: Прайс-лист"), state=StateGroupFSM.user_state_admin)
async def buttonContactMess(message: types.Message):
    """ Отвечает на кнопку 'Редактировать: Прайс-лист'. 
    Переводит пользователя администратора в состояние:
    жду ввод текста 'Редактировать: Прайс-лист'. """
    await message.answer('Редактирование пункта: Прайс-лист. Введите новый текст.')
    await StateGroupFSM.user_state_admin_edit_price.set()


@dp.message_handler(Text(equals="Ред: Контакты"), state=StateGroupFSM.user_state_admin)
async def buttonContactMess(message: types.Message):
    """ Отвечает на кнопку 'Редактировать: Контакты'. 
    Переводит пользователя администратора в состояние:
    жду ввод текста 'Редактировать: Контакты'. """
    await message.answer('Редактирование пункта: Контакты. Введите новый текст.')
    await StateGroupFSM.user_state_admin_edit_contact.set()


@dp.message_handler(Text(equals="Ред: Расписание"), state=StateGroupFSM.user_state_admin)
async def buttonContactMess(message: types.Message):
    """ Отвечает на кнопку 'Редактировать: Расписание'. 
    Переводит пользователя администратора в состояние:
    админка, жду картинку 'Расписание' """
    await message.answer('Редактирование пункта: Расписание. Отправьте новую картинку.')
    await StateGroupFSM.user_state_admin_edit_image.set()


@dp.message_handler(Text(equals="Ред: Афиша"), state=StateGroupFSM.user_state_admin)
async def buttonContactMess(message: types.Message):
    """ Отвечает на кнопку 'Редактировать: Афиша'. 
    Переводит пользователя администратора в состояние:
    админка, жду картинку 'Афиша' """
    await message.answer('Редактирование пункта: Афиша. Отправьте новую картинку.')
    await StateGroupFSM.user_state_admin_edit_poster.set()
###################################################################################################


@dp.message_handler(state=StateGroupFSM.user_state_admin_edit_about)
async def buttonContactMess(message: types.Message):
    """ Отвечает на любые сообщения в состоятии:  жду ввод текста 'О нас'. 
    Возвращает пользователя администратора в состояние: admin. """
    await message.answer(func.ExecuteSQL_update(1, message.text))
    await message.answer('Пункт Отредактирован')
    await StateGroupFSM.user_state_admin.set()


@dp.message_handler(state=StateGroupFSM.user_state_admin_edit_price)
async def buttonContactMess(message: types.Message):
    """ Отвечает на любые сообщения в состоятии:  жду ввод текста 'Прайс-лист'. 
    Возвращает пользователя администратора в состояние: admin. """
    await message.answer(func.ExecuteSQL_update(2, message.text))
    await message.answer('Пункт Отредактирован')
    await StateGroupFSM.user_state_admin.set()


@dp.message_handler(state=StateGroupFSM.user_state_admin_edit_contact)
async def buttonContactMess(message: types.Message):
    """ Отвечает на любые сообщения в состоятии:  жду ввод текста 'Контакты'. 
    Возвращает пользователя администратора в состояние: admin. """
    await message.answer(func.ExecuteSQL_update(3, message.text))
    await message.answer('Пункт Отредактирован')
    await StateGroupFSM.user_state_admin.set()


###################################################################################################
# Редактирование картинок в админке

# Известные типы сообщения: TEXT, AUDIO, DOCUMENT, GAME, PHOTO, STICKER, VIDEO, VOICE,
# NEW_CHAT_MEMBERS, LEFT_CHAT_MEMBER, INVOICE, SUCCESSFUL_PAYMENT, UNKNOWN.
###################################################################################################
@dp.message_handler(state=StateGroupFSM.user_state_admin_edit_image)
@dp.message_handler(content_types=['photo'], state=StateGroupFSM.user_state_admin_edit_image)
@dp.message_handler(content_types=['document'], state=StateGroupFSM.user_state_admin_edit_image)
async def edit_img_timetable(message: types.Message):
    """ Редактирование 'Расписание'.
    
    Отвечает на любые сообщения, документы и картинки в состоятии:
    "админка, жду картинку 'Расписание'".
    Осуществляет проверку, что отправил пользователь, какой тип сообщения.
    Если отправленна картинка, запускаем остальной код:
    Сохраняет отправленную пользователем-админум картинку в корне на диске
    под именем img.jpg, потом вызывает удалённую функцию отправки картинки в BD.
    Возвращает пользователя администратора в состояние: admin. """

    cont_type = message.content_type
    print(cont_type)

    if cont_type == 'photo':
        await message.photo[-1].download('img.jpg')
        func.ExecuteSQL_Image_update('timetable')
        await message.answer('Пункт отредактирован')
        await StateGroupFSM.user_state_admin.set()
    else:
        await message.answer('Необходимо отправить картинку.' +
        ' Установите галочку "Сжать изображение".')


@dp.message_handler(state=StateGroupFSM.user_state_admin_edit_poster)
@dp.message_handler(content_types=['photo'], state=StateGroupFSM.user_state_admin_edit_poster)
@dp.message_handler(content_types=['document'], state=StateGroupFSM.user_state_admin_edit_poster)
async def edit_img_poster(message: types.Message):
    """ Редактирование 'Афиша'.
    
    Отвечает на любые сообщения, документы и картинки в состоятии:
    "админка, жду картинку 'Афиша'".
    Осуществляет проверку, что отправил пользователь, какой тип сообщения.
    Если отправленна картинка, запускаем остальной код:
    Сохраняет отправленную пользователем-админум картинку в корне на диске
    под именем img.jpg, потом вызывает удалённую функцию отправки картинки в BD.
    Возвращает пользователя администратора в состояние: admin. """

    cont_type = message.content_type
    print(cont_type)

    if cont_type == 'photo':
        await message.photo[-1].download('img.jpg')
        func.ExecuteSQL_Image_update('poster')
        await message.answer('Пункт отредактирован')
        await StateGroupFSM.user_state_admin.set()
    else:
        await message.answer('Необходимо отправить картинку.' +
        ' Установите галочку "Сжать изображение".')
###################################################################################################


@dp.message_handler(state=StateGroupFSM.user_state_default)
async def all_mess_state_default(message: types.Message):
    """ Отвечает на любые сообщения, если состояние не default.
    reply_markup=keyboard - показывает клавиатуру """
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