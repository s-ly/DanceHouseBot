###################################################################################################
# NOTE
###################################################################################################
# Телеграм бот школы танцев t.me/DanceHouseBot
# Версия 1.1 дата 2022.06.26
# Главный модуль

# Файлы и папки (только рабочие):
    # app.py - главный модуль
    # admin.py - главный модуль админки
    # func.py - модуль с методами
    # sql.py - работа с БД
    # MyToken.py - хранит токены
    # DanceHouseBot.db - база данных
    # templates
        # base.html - базовый шаблон для админки
        # index.html - шаблон для index.html
        # new_text.html - шаблон отредактрованного текста
        # new_img.html - шаблон загруженных картинок
###################################################################################################


from email import message
# from re import X
from unittest.mock import call
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
import sql             # мой модуль работы с БД


###################################################################################################
# Переключение токенов
###################################################################################################
# Файл MyToken.py содержит две строки:
# myToken = 'тут токен'
# testToken = 'тут токен'
# При разработке использеум test, для работы my.
# в git его игнорируем, а в место пушим зашифрованный архив.

API_TOKEN = MyToken.myToken # рабочий бот
# API_TOKEN = MyToken.testToken # тестовый бот
###################################################################################################


# Initialize bot and dispatcher
storage = MemoryStorage() # место хранения контекста в ОЗУ
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


# создаём состояния
class StateGroupFSM(StatesGroup):
    user_state_admin = State()  # для админки
    user_state_default = State()  # все остальные
    user_state_waiting_contacts = State()  # жду контакты
    user_state_admin_edit_about = State()  # для админки, жду ввод текста 'О нас'
    user_state_admin_edit_price = State()  # для админки, жду ввод текста 'Прайс-лист'
    user_state_admin_edit_contact = State()  # для админки, жду ввод текста 'Контакты'
    user_state_admin_edit_image = State()  # админка, жду картинку 'Расписание'
    user_state_admin_edit_poster = State()  # админка, жду картинку 'Афиша'


async def InItStateUser(message: types.Message, state: FSMContext):
    """ Инициирует данные пользователя """        
    await state.update_data(userID=message.chat.id)
    await state.update_data(userName=message.chat.username)
    await state.update_data(firstName=message.chat.first_name)
    await state.update_data(lastName=message.chat.last_name)
    await state.update_data(userDanceSelect='not selected')
    await state.update_data(userDaySelect='not selected')
    await state.update_data(userContac='no')
    func.Print_LOG("Инициирует данные пользователя")


###################################################################################################
# Клавиатуры
###################################################################################################
# создаём коавиатуру и добавляем кнопки
# resize_keyboard=True - уменьшает кнопки
# one_time_keyboard=True - скрыть кнопку после нажатия
# keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
# keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
keyboard = ReplyKeyboardMarkup(resize_keyboard=True)
button_main = KeyboardButton('На главную')
button_about = KeyboardButton('О нас')
button_price = KeyboardButton('Прайс-лист')
button_contact = KeyboardButton('Контакты')
button_timetable = KeyboardButton('Расписание')
button_poster = KeyboardButton('Афиша')
keyboard.add(button_main, button_about, button_price, button_contact, button_timetable, button_poster)


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


# Инлайн-клавиатура для квиза, шаг-1 (Здравствуйте)
inline_key_kviz_step1 = types.InlineKeyboardMarkup()

inline_but_kviz_step1_b1 = types.InlineKeyboardButton(
    text='Как записаться на пробное занятие?',
    callback_data='s1b1')
inline_but_kviz_step1_b2 = types.InlineKeyboardButton(
    text='Расписание',
    callback_data='s1b2')
inline_but_kviz_step1_b3 = types.InlineKeyboardButton(
    text='Я без пары и танцевального опыта, как быть?',
    callback_data='s1b3')
inline_but_kviz_step1_b4 = types.InlineKeyboardButton(
    text='Где Вы находитесь?',
    callback_data='s1b4')
inline_but_kviz_step1_b5 = types.InlineKeyboardButton(
    text='Сколько это стоит?',
    callback_data='s1b5')

inline_key_kviz_step1.add(inline_but_kviz_step1_b1)
inline_key_kviz_step1.add(inline_but_kviz_step1_b2)
inline_key_kviz_step1.add(inline_but_kviz_step1_b3)
inline_key_kviz_step1.add(inline_but_kviz_step1_b4)
inline_key_kviz_step1.add(inline_but_kviz_step1_b5)


# Инлайн-клавиатура для квиза, шаг-2 (Как записаться)
inline_key_kviz_step2 = types.InlineKeyboardMarkup()

inline_but_kviz_step2_b1 = types.InlineKeyboardButton(
    text='В паре',
    callback_data='s2b1')
inline_but_kviz_step2_b2 = types.InlineKeyboardButton(
    text='Начну сольно (только для девушек)',
    callback_data='s2b2')
inline_but_kviz_step2_b3 = types.InlineKeyboardButton(
    text='Хочу в паре, но пары нет',
    callback_data='s2b3')

inline_key_kviz_step2.add(inline_but_kviz_step2_b1)
inline_key_kviz_step2.add(inline_but_kviz_step2_b2)
inline_key_kviz_step2.add(inline_but_kviz_step2_b3)


# Инлайн-клавиатура для квиза, шаг-3 (Выбор танца)
inline_key_kviz_step3 = types.InlineKeyboardMarkup()

inline_but_kviz_step3_b1 = types.InlineKeyboardButton(
    text='Бачата',
    callback_data='s3b1')
inline_but_kviz_step3_b2 = types.InlineKeyboardButton(
    text='Сальса',
    callback_data='s3b2')
inline_but_kviz_step3_b3 = types.InlineKeyboardButton(
    text='Кизомба',
    callback_data='s3b3')
inline_but_kviz_step3_b4 = types.InlineKeyboardButton(
    text='Пока не разбираюсь',
    callback_data='s3b4')

inline_key_kviz_step3.add(inline_but_kviz_step3_b1)
inline_key_kviz_step3.add(inline_but_kviz_step3_b2)
inline_key_kviz_step3.add(inline_but_kviz_step3_b3)
inline_key_kviz_step3.add(inline_but_kviz_step3_b4)


# Инлайн-клавиатура для квиза, шаг-4 (Выбор дня и времени)
inline_key_kviz_step4_dance1 = types.InlineKeyboardMarkup()
inline_key_kviz_step4_dance2 = types.InlineKeyboardMarkup()
inline_key_kviz_step4_dance3 = types.InlineKeyboardMarkup()
inline_key_kviz_step4_dance4 = types.InlineKeyboardMarkup()

inline_but_kviz_step4_b1 = types.InlineKeyboardButton(
    text='Вторник 19:00',
    callback_data='s4b1')
inline_but_kviz_step4_b2 = types.InlineKeyboardButton(
    text='Суббота 19:00',
    callback_data='s4b2')
inline_but_kviz_step4_b3 = types.InlineKeyboardButton(
    text='Среда 19:30',
    callback_data='s4b3')
inline_but_kviz_step4_b4 = types.InlineKeyboardButton(
    text='Пятница 19:30',
    callback_data='s4b4')
inline_but_kviz_step4_b5 = types.InlineKeyboardButton(
    text='Понедельник 20:30',
    callback_data='s4b5')
inline_but_kviz_step4_b6 = types.InlineKeyboardButton(
    text='Четверг 20:30',
    callback_data='s4b6')
inline_but_kviz_step4_b7 = types.InlineKeyboardButton(
    text='Среда 18:30',
    callback_data='s4b7')
inline_but_kviz_step4_b8 = types.InlineKeyboardButton(
    text='Пятница 18:30',
    callback_data='s4b8')

# Бачата
inline_key_kviz_step4_dance1.add(inline_but_kviz_step4_b1)
inline_key_kviz_step4_dance1.add(inline_but_kviz_step4_b2)

# Сальса
inline_key_kviz_step4_dance2.add(inline_but_kviz_step4_b3)
inline_key_kviz_step4_dance2.add(inline_but_kviz_step4_b4)

# Кизомба
inline_key_kviz_step4_dance3.add(inline_but_kviz_step4_b5)
inline_key_kviz_step4_dance3.add(inline_but_kviz_step4_b6)

# Lady Style
inline_key_kviz_step4_dance4.add(inline_but_kviz_step4_b7)
inline_key_kviz_step4_dance4.add(inline_but_kviz_step4_b8)


# Инлайн-клавиатура для квиза, шаг-5 (заполнение формы)
inline_key_kviz_step5 = types.InlineKeyboardMarkup()

inline_but_kviz_step5_b1 = types.InlineKeyboardButton(
    text='Оставить заявку',
    callback_data='s5b1')

inline_but_kviz_step5_b2 = types.InlineKeyboardButton(
    text='Выбрать другое',
    callback_data='s5b2')

inline_key_kviz_step5.add(inline_but_kviz_step5_b1)
inline_key_kviz_step5.add(inline_but_kviz_step5_b2)

# Инлайн-клавиатура для квиза, шаг-6 (вернуться в начало)
inline_key_kviz_step6 = types.InlineKeyboardMarkup()

inline_but_kviz_step6_b1 = types.InlineKeyboardButton(
    text='Вернуться в начало',
    callback_data='s6b1')

inline_key_kviz_step6.add(inline_but_kviz_step6_b1)
###################################################################################################


@dp.message_handler(commands=['test'], state=StateGroupFSM.user_state_default)
async def sendFormAdmin(message: types.Message, state: FSMContext):
    """ отправить анкету админу """
    func.Print_LOG("отправить анкету админу")
    form = await func.createFormAdmin(message, state)
    admin_id = 80315171 # я, Вероника 1837933533
    admin_id_vladimir = 434967278 # id Владимира
    admin_id_linda = 1170918217 # id Линды
    await bot.send_message(admin_id, form)
    await bot.send_message(admin_id_vladimir, form)
    await bot.send_message(admin_id_linda, form)


@dp.message_handler(commands=['start'], state='*')
async def start(message: types.Message, state: FSMContext):
    """ Отвечает на команду: /start когда состояние пользователя не установлено.
    Устанавливает состояние пользователя на user_state_default."""
    text_hello = 'Здравствуйте!'
    await InItStateUser(message, state) # Инициирует данные пользователя
    await StateGroupFSM.user_state_default.set() # Инициирует состояние пользователя
    # await message.answer(func.ExecuteSQL(4), reply_markup=keyboard) 
    await message.answer(text_hello, reply_markup=keyboard) 
    await message.answer(sql.sql_read_text(4, 'message'), reply_markup=inline_key_kviz_step1)


@dp.message_handler(commands=['gs'], state='*')
async def get_state(message: types.Message, state: FSMContext):
    """ Узнать текущий статус состояния"""
    cs = await state.get_state()
    await message.answer(str(cs))
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


@dp.message_handler(state=StateGroupFSM.user_state_waiting_contacts)
async def waitingContacts(message: types.Message, state: FSMContext):
    """ Перехватывает всё в состояниии 'Жду контактов' """
    await state.update_data(userContac=message.text)
    textForm = await func.confirmationForm(message, state)
    # await message.answer(textForm)
    await message.answer(textForm, reply_markup=inline_key_kviz_step5)
    await StateGroupFSM.user_state_default.set() # Инициирует состояние пользователя default    


###################################################################################################
# Обработка инлайн кнопок квиза
#
# Передаём message в await start(call_inline.message) так-как он нужен методу start()
###################################################################################################
# Шаг 1
@dp.callback_query_handler(text='s1b1', state=StateGroupFSM.user_state_default)
async def callback_inline_but_s1b1(call_inline: types.CallbackQuery):
    """ Обработка inline-кнопки s1b1 (Как записаться). Переходит к шаг-2."""
    func.Print_LOG("Обработка inline-кнопки s1b1 (Как записаться)")
    await call_inline.answer('Хорошо')
    text = "Вы хотели бы танцевать в паре или сольно?"
    await call_inline.message.answer(text, reply_markup=inline_key_kviz_step2)


@dp.callback_query_handler(text='s1b2', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery):
    """ Обработка inline-кнопки s1b2 (Расписание).

    Показывает расписание а потом переходит к шаг-2.
    Сам показ работает так, словно нажата обычная кнопка 'Расписание'.
    В конце вызывается метод, как если бы нажали инлайн-кнопку 's1b1 (Как записаться)'."""
    func.Print_LOG("Обработка inline-кнопки s1b2 (Расписание)")
    await call_inline.answer('Хорошо')    
    text = "Стоимость пробного урока 350 руб"
    await call_inline.message.answer(text)
    await buttonTimetable(call_inline.message)  # показ расписания
    await callback_inline_but_s1b1(call_inline) # прыжек на Шаг 1


@dp.callback_query_handler(text='s1b3', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery):
    """ Обработка inline-кнопки s1b3 (Я без пары и).

    В конце вызывается метод, как если бы нажали инлайн-кнопку 's1b1 (Как записаться)'."""
    func.Print_LOG("Обработка inline-кнопки s1b3 (Я без пары и)")
    await call_inline.answer('Хорошо')    
    text = ("Наличие пары не обязательно. Подберем на занятии. " +
    "Есть группа сольного направления Леди Стайл. (только для девушек). " +
    "Танцевальный опыт не нужен. Обучаем с Нуля.")
    await call_inline.message.answer(text)
    await callback_inline_but_s1b1(call_inline) # прыжек на Шаг 1


@dp.callback_query_handler(text='s1b4', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery):
    """ Обработка inline-кнопки s1b4 (Где Вы).

    В конце вызывается метод, как если бы нажали инлайн-кнопку 's1b1 (Как записаться)'."""
    func.Print_LOG("Обработка inline-кнопки s1b4 (Где Вы)")
    await call_inline.answer('Хорошо')   
    text = "Наш адрес Щапова 47, 1 этаж, 102 офис."
    await call_inline.message.answer(text) 
    await callback_inline_but_s1b1(call_inline) # прыжек на Шаг 1


@dp.callback_query_handler(text='s1b5', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery):
    """ Обработка inline-кнопки s1b5 (Сколько это стоит).

    В конце вызывается метод, как если бы нажали инлайн-кнопку 's1b1 (Как записаться)'."""
    func.Print_LOG("Обработка inline-кнопки s1b5 (Сколько это стоит)")
    await call_inline.answer('Хорошо')    
    text = ("Пробный урок 350 руб. " +
    "По итогам пробного урока вам будут предложены различные виды абонементы")
    await call_inline.message.answer(text) 
    await callback_inline_but_s1b1(call_inline) # прыжек на Шаг 1


# Шаг 2
@dp.callback_query_handler(text='s2b1', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки s2b1 (В паре)"""
    func.Print_LOG("Обработка inline-кнопки s2b1 (В паре)")
    await call_inline.answer('Хорошо')  
    text = ("Выберите направление танца")  
    # await call_inline.message.answer(text)
    await call_inline.message.answer(text, reply_markup=inline_key_kviz_step3)


@dp.callback_query_handler(text='s2b2', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки s2b2 (Начну сольно (только для девушек))"""
    func.Print_LOG("Обработка inline-кнопки s2b2 (Начну сольно (только для девушек)")
    text = """Бачата Lady Style - танцевальное направление для всех девушек,
    которые хотят научиться красиво двигаться под любую музыку, быть пластичными,
    гибкими и артистичными. Танцы, как ничто иное, помогают избавиться от комплексов
    и полюбить свое тело.
    Расписание занятий начинающей группы по Lady Style:
    Среда 18:30
    Пятница 18:30
    Стоимость пробного урока 350р
    На какой день вас записать?"""
    await call_inline.answer('Хорошо')    
    await state.update_data(userDanceSelect='Lady Style')
    # await sendFormAdmin(call_inline.message, state)
    await call_inline.message.answer(text, reply_markup=inline_key_kviz_step4_dance4)


@dp.callback_query_handler(text='s2b3', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки s2b3 (Хочу в паре, но пару нет)"""
    func.Print_LOG("Обработка inline-кнопки s2b3 (Хочу в паре, но пару нет)")
    await call_inline.answer('Хорошо')    
    text = ("Наличие пары не обязательно. " +
    "Подберем на занятии. Выберите направление танца")  
    # await call_inline.message.answer(text)
    await call_inline.message.answer(text, reply_markup=inline_key_kviz_step3)


# Шаг 3
@dp.callback_query_handler(text='s3b1', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки s3b1 (Бачата)"""
    func.Print_LOG("Обработка inline-кнопки s3b1 (Бачата)")
    text = """Расписание занятий начинающей группы по Бачате:
    Вторник 19:00
    Суббота 19:00
    Стоимость пробного урока 350р
    На какой день вас записать?"""
    await call_inline.answer('Хорошо')
    await state.update_data(userDanceSelect='Бачата')
    # await sendFormAdmin(call_inline.message, state)
    await call_inline.message.answer(text, reply_markup=inline_key_kviz_step4_dance1)


@dp.callback_query_handler(text='s3b2', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки s3b2 (Сальса)"""
    func.Print_LOG("Обработка inline-кнопки s3b2 (Сальса)")
    text = """Расписание занятий начинающей группы по Сальсе:
    Среда 19:30
    Пятница 19:30
    Стоимость пробного урока 350р
    На какой день вас записать?"""
    await call_inline.answer('Хорошо')
    await state.update_data(userDanceSelect='Сальса')
    # await sendFormAdmin(call_inline.message, state)
    await call_inline.message.answer(text, reply_markup=inline_key_kviz_step4_dance2)


@dp.callback_query_handler(text='s3b3', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки s3b3 (Кизомба)"""
    func.Print_LOG("Обработка inline-кнопки s3b3 (Кизомба)")
    text = """Расписание занятий начинающей группы по Кизомбе:
    Понедельник 20:30
    Четверг 20:30
    Стоимость пробного урока 350р
    На какой день вас записать?"""
    await call_inline.answer('Хорошо')
    await state.update_data(userDanceSelect='Кизомба')
    # await sendFormAdmin(call_inline.message, state)
    await call_inline.message.answer(text, reply_markup=inline_key_kviz_step4_dance3)


@dp.callback_query_handler(text='s3b4', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки s3b4 (Пока не разбираюсь)"""
    func.Print_LOG("Обработка inline-кнопки s3b4 (Пока не разбираюсь)")    
    await call_inline.answer('Хорошо')
    text = """
Бачата — это демонстрация мужественности и силы партнёра по отношению
к женственности и соблазнительности партнёрши.
Бачата имеет упрощенную хореографию, поэтому этот танец отлично подходит
в качестве танца для начинающих. Но, несмотря на всю свою простоту и легкость,
бачата является довольно разнообразным и богатым техникой танцем.

Современная кизомба – это сексуальный непринужденный танец,
который позволяет чувствовать своего партнера, малейшие его движения и желания.
Кизомба не без причины назван самым сексуальным танцем 21 века и находится на пике
популярности, ее танцуют в ночных клубах, на дискотеках, на вечеринках!

Сальса помогает проще относиться к жизни! Кубинцы говорят, что европейцы танцуют
сальсу потому, что хотят научиться у кубинцев веселиться. И это абсолютная правдаМы,
жители холодного и неприветливого климата совершенно забыли, что для развлечения и
веселья нужно всего-то: музыка, азарт и улыбка.

Выберите направление танца
"""
    await call_inline.message.answer(text, reply_markup=inline_key_kviz_step3)


# Шаг 4 (выбор дня и времени)
@dp.callback_query_handler(text='s4b1', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки выбора дня недели и времени s4b1 """
    func.Print_LOG("Обработка inline-кнопки выбора дня недели и времени s4b1")
    await call_inline.answer('Хорошо')
    await state.update_data(userDaySelect=inline_but_kviz_step4_b1.text) # берём из кнопки
    text = ('Напишите Ваш номер телефона и имя. В течении суток с вами свяжется ваш тренер. '
    + 'В конце нажмите кнопку «Оставить заявку».')
    await call_inline.message.answer(text)
    await StateGroupFSM.user_state_waiting_contacts.set() # состояние: жду контакты


@dp.callback_query_handler(text='s4b2', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки выбора дня недели и времени s4b2 """
    func.Print_LOG("Обработка inline-кнопки выбора дня недели и времени s4b2")
    await call_inline.answer('Хорошо')
    await state.update_data(userDaySelect=inline_but_kviz_step4_b2.text) # берём из кнопки
    text = ('Напишите Ваш номер телефона и имя. В течении суток с вами свяжется ваш тренер. '
    + 'В конце нажмите кнопку «Оставить заявку».')
    await call_inline.message.answer(text)
    await StateGroupFSM.user_state_waiting_contacts.set() # состояние: жду контакты


@dp.callback_query_handler(text='s4b3', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки выбора дня недели и времени s4b3 """
    func.Print_LOG("Обработка inline-кнопки выбора дня недели и времени s4b3")
    await call_inline.answer('Хорошо')
    await state.update_data(userDaySelect=inline_but_kviz_step4_b3.text) # берём из кнопки
    text = ('Напишите Ваш номер телефона и имя. В течении суток с вами свяжется ваш тренер. '
    + 'В конце нажмите кнопку «Оставить заявку».')
    await call_inline.message.answer(text)
    await StateGroupFSM.user_state_waiting_contacts.set() # состояние: жду контакты

@dp.callback_query_handler(text='s4b4', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки выбора дня недели и времени s4b4 """
    func.Print_LOG("Обработка inline-кнопки выбора дня недели и времени s4b4")
    await call_inline.answer('Хорошо')
    await state.update_data(userDaySelect=inline_but_kviz_step4_b4.text) # берём из кнопки
    text = ('Напишите Ваш номер телефона и имя. В течении суток с вами свяжется ваш тренер. '
    + 'В конце нажмите кнопку «Оставить заявку».')
    await call_inline.message.answer(text)
    await StateGroupFSM.user_state_waiting_contacts.set() # состояние: жду контакты

@dp.callback_query_handler(text='s4b5', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки выбора дня недели и времени s4b5 """
    func.Print_LOG("Обработка inline-кнопки выбора дня недели и времени s4b5")
    await call_inline.answer('Хорошо')
    await state.update_data(userDaySelect=inline_but_kviz_step4_b5.text) # берём из кнопки
    text = ('Напишите Ваш номер телефона и имя. В течении суток с вами свяжется ваш тренер. '
    + 'В конце нажмите кнопку «Оставить заявку».')
    await call_inline.message.answer(text)
    await StateGroupFSM.user_state_waiting_contacts.set() # состояние: жду контакты


@dp.callback_query_handler(text='s4b6', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки выбора дня недели и времени s4b6 """
    func.Print_LOG("Обработка inline-кнопки выбора дня недели и времени s4b6")
    await call_inline.answer('Хорошо')
    await state.update_data(userDaySelect=inline_but_kviz_step4_b6.text) # берём из кнопки
    text = ('Напишите Ваш номер телефона и имя. В течении суток с вами свяжется ваш тренер. '
    + 'В конце нажмите кнопку «Оставить заявку».')
    await call_inline.message.answer(text)
    await StateGroupFSM.user_state_waiting_contacts.set() # состояние: жду контакты


@dp.callback_query_handler(text='s4b7', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки выбора дня недели и времени s4b7 """
    func.Print_LOG("Обработка inline-кнопки выбора дня недели и времени s4b7")
    await call_inline.answer('Хорошо')
    await state.update_data(userDaySelect=inline_but_kviz_step4_b7.text) # берём из кнопки
    text = ('Напишите Ваш номер телефона и имя. В течении суток с вами свяжется ваш тренер. '
    + 'В конце нажмите кнопку «Оставить заявку».')
    await call_inline.message.answer(text)
    await StateGroupFSM.user_state_waiting_contacts.set() # состояние: жду контакты


@dp.callback_query_handler(text='s4b8', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки выбора дня недели и времени s4b8 """
    func.Print_LOG("Обработка inline-кнопки выбора дня недели и времени s4b8")
    await call_inline.answer('Хорошо')
    await state.update_data(userDaySelect=inline_but_kviz_step4_b8.text) # берём из кнопки
    text = ('Напишите Ваш номер телефона и имя. В течении суток с вами свяжется ваш тренер. '
    + 'В конце нажмите кнопку «Оставить заявку».')
    await call_inline.message.answer(text)
    await StateGroupFSM.user_state_waiting_contacts.set() # состояние: жду контакты


# Шаг 5 (отправка формы)
@dp.callback_query_handler(text='s5b1', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки Записаться s5b1 """
    func.Print_LOG("Обработка inline-кнопки Записаться s5b1")
    await call_inline.answer('Хорошо')
    await sendFormAdmin(call_inline.message, state)
    text = """Ваша заявка принята. Мы с вами свяжемся в течение суток."""
    await call_inline.message.answer(text, reply_markup=inline_key_kviz_step6) 
    # await start(call_inline.message, state) # на старт
    # await call_inline.message.answer(text, reply_markup=inline_key_kviz_step4_dance3)


@dp.callback_query_handler(text='s5b2', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки Выбрать другое s5b2 """
    func.Print_LOG("Обработка inline-кнопки Выбрать другое s5b2")
    await call_inline.answer('Хорошо')
    await start(call_inline.message, state) # на старт


# Шаг 6 (вернуться в начало)
@dp.callback_query_handler(text='s6b1', state=StateGroupFSM.user_state_default)
async def process_callback_button1(call_inline: types.CallbackQuery, state: FSMContext):
    """ Обработка inline-кнопки Вернуться в начало s6b1 """
    func.Print_LOG("Обработка inline-кнопки Вернуться в начало s6b1")
    await call_inline.answer('Хорошо')
    await start(call_inline.message, state) # на старт


###################################################################################################
# Показ данных
###################################################################################################
@dp.message_handler(Text(equals="Показ: Афиша"), state=StateGroupFSM.user_state_admin)
@dp.message_handler(Text(equals="Афиша"), state=StateGroupFSM.user_state_default)
async def buttonTimetableMess(message: types.Message):
    """ Показывает Афишу. """
    func.Print_LOG("кнопка афиша")
    # photo = func.ExecuteSQL_getImage('poster')
    photo = sql.sql_read_img('poster')
    await bot.send_photo(message.from_user.id, photo)


@dp.message_handler(Text(equals="Показ: Расписание"), state=StateGroupFSM.user_state_admin)
@dp.message_handler(Text(equals="Расписание"), state=StateGroupFSM.user_state_default)
async def buttonTimetable(message: types.Message):
    """ Показывает Расписание.
    
    До того как я спользовал инлайн-кнопку кнопку s1b2 (Расписание),
    работал такой метод: await bot.send_photo(message.from_user.id, photo),
    но с добвлением кнопки я переделал метод на текущий, так-как иначе вызов
    этого метода из инлаайн-кнопки s1b2 не работал. В ошибке говорилось
    о том, что бот не может писать боту. То-есть из простой кнопки работало,
    а из инлайн нет. Но теперь работает в обоих случаях. Тоесть в место
    from_user.id я использую chat.id."""
    func.Print_LOG("кнопка Расписание")
    # photo = func.ExecuteSQL_getImage('timetable')
    photo = sql.sql_read_img('timetable')
    await bot.send_photo(message.chat.id, photo)


@dp.message_handler(Text(equals="Показ: О нас"), state=StateGroupFSM.user_state_admin)
@dp.message_handler(Text(equals="О нас"), state=StateGroupFSM.user_state_default)
async def buttonAboutMess(message: types.Message):
    """ Показывает О нас. """
    # await message.answer(func.ExecuteSQL(1))
    await message.answer(sql.sql_read_text(1, 'message'))


@dp.message_handler(Text(equals="Показ: Прайс-лист"), state=StateGroupFSM.user_state_admin)
@dp.message_handler(Text(equals="Прайс-лист"), state=StateGroupFSM.user_state_default)
async def buttonPriceMess(message: types.Message):
    """ Показывает Прайс-лист.
    # code(...) и parse_mode=... форматируют текст моноширно. """
    # await message.answer(code(func.ExecuteSQL(2)), parse_mode=types.ParseMode.MARKDOWN_V2)
    await message.answer(code(sql.sql_read_text(2, 'message')), parse_mode=types.ParseMode.MARKDOWN_V2)


@dp.message_handler(Text(equals="Показ: Контакты"), state=StateGroupFSM.user_state_admin)
@dp.message_handler(Text(equals="Контакты"), state=StateGroupFSM.user_state_default)
async def buttonContactMess(message: types.Message):
    """ Показывает Контакты.
    Дополнительно показывает инлайн-клавиатуру."""
    # await message.answer(func.ExecuteSQL(3), reply_markup=inline_key_contacts)
    await message.answer(sql.sql_read_text(3, 'message'), reply_markup=inline_key_contacts)
    print('кнопка отправленна')


@dp.message_handler(Text(equals="На главную"), state=StateGroupFSM.user_state_default)
async def buttonAboutMess(message: types.Message, state: FSMContext):
    """ Обрабатывает 'На главную'. """
    await start(message, state)
    func.Print_LOG("Переброска на Start (На главную)")


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
    # await message.answer(func.ExecuteSQL_update(1, message.text))
    await message.answer(sql.ExecuteSQL_update(1, message.text))
    await message.answer('Пункт Отредактирован')
    await StateGroupFSM.user_state_admin.set()


@dp.message_handler(state=StateGroupFSM.user_state_admin_edit_price)
async def buttonContactMess(message: types.Message):
    """ Отвечает на любые сообщения в состоятии:  жду ввод текста 'Прайс-лист'. 
    Возвращает пользователя администратора в состояние: admin. """
    # await message.answer(func.ExecuteSQL_update(2, message.text))
    await message.answer(sql.ExecuteSQL_update(2, message.text))
    await message.answer('Пункт Отредактирован')
    await StateGroupFSM.user_state_admin.set()


@dp.message_handler(state=StateGroupFSM.user_state_admin_edit_contact)
async def buttonContactMess(message: types.Message):
    """ Отвечает на любые сообщения в состоятии:  жду ввод текста 'Контакты'. 
    Возвращает пользователя администратора в состояние: admin. """
    # await message.answer(func.ExecuteSQL_update(3, message.text))
    await message.answer(sql.ExecuteSQL_update(3, message.text))
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
        # func.ExecuteSQL_Image_update('timetable')
        sql.ExecuteSQL_Image_update('timetable')
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
        # func.ExecuteSQL_Image_update('poster')
        sql.ExecuteSQL_Image_update('poster')
        await message.answer('Пункт отредактирован')
        await StateGroupFSM.user_state_admin.set()
    else:
        await message.answer('Необходимо отправить картинку.' +
        ' Установите галочку "Сжать изображение".')
###################################################################################################


@dp.message_handler(state=StateGroupFSM.user_state_default)
async def all_mess_state_default(message: types.Message):
    """ Отвечает на любые сообщения, если состояние default.
    reply_markup=keyboard - показывает клавиатуру """
    await message.answer('Используйте кнопки.', reply_markup=keyboard)


@dp.message_handler()
async def all_mess_state_default(message: types.Message, state: FSMContext):
    """ Отвечает на любые сообщения, если состояние не default"""    
    await start(message, state)
    func.Print_LOG("Переброска на Start")


@dp.message_handler(state=StateGroupFSM.user_state_admin)
async def allMess(message: types.Message):
    """ Отвечает на любые сообщения в админке.
    Перехватывает состояние user_state_admin."""
    await message.answer('Используйте кнопки для админки.')


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)