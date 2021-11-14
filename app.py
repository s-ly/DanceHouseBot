# Телеграм бот t.me/DanceHouseBot
# Школа танцев.

from aiogram import Bot, Dispatcher, executor, types
import MyToken  # содержит токен

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




@dp.message_handler()
async def allMess(message: types.Message):
    """ Отвечает на любые сообщения."""
    await message.answer('test ok')




if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)