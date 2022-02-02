# from _typeshed import Self
# from typing_extensions import Self
from aiogram import Bot, Dispatcher, executor, types
import MyToken  # содержит токен




class MyClass:
    def __init__(self) -> None:
        # Импрорт токена из файла MyToken.py (лежит в раб каталоге)
        # Файл MyToken.py содержит две строки:
        # myToken = 'тут токен'
        # testToken = 'тут токен'
        # При разработке использеум test, для работы my.
        # в git его игнорируем, а в место пушим зашифрованный архив.
        # API_TOKEN = MyToken.myToken # рабочий бот
        self.API_TOKEN = MyToken.testToken # тестовый бот

        # Initialize bot and dispatcher
        self.bot = Bot(token=self.API_TOKEN)
        self.dp = Dispatcher(self.bot)




    @dp.message_handler()
    # @dp.message_handler()
    async def allMess(message: types.Message):
        """ Отвечает на любые сообщения."""
        await message.answer('test ok')



mybot = MyClass()
if __name__ == '__main__':
    executor.start_polling(mybot.dp, skip_updates=True)