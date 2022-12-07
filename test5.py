# Тестовый бот для отработки скрытия текстов
# В FSMContext для каждого пользователя храним id сообщения,
# и по этому сообщению его удаляем.

from aiogram import Bot, Dispatcher, executor, types
# from aiogram.methods.delete_message import DeleteMessage
# from aiogram import DeleteMessage
import MyToken  # содержит токен


# хранение контекста
from aiogram.dispatcher import FSMContext 

# место для хранения контекста в ОЗУ
from aiogram.contrib.fsm_storage.memory import MemoryStorage 


API_TOKEN = MyToken.testToken # тестовый бот
storage = MemoryStorage() # место хранения контекста в ОЗУ
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot, storage=storage)


async def InItStateUser(message: types.Message, state: FSMContext):
    """ Инициирует данные пользователя """        
    await state.update_data(userID=message.chat.id)
    await state.update_data(test=[])
    await state.update_data(bot_mes=[])


@dp.message_handler(commands=['del'])
async def start2(message: types.Message, state: FSMContext):
    """
    Удаляет все сообщения по id.
    В конце инициирует (обнудяет) базу id.
    """
    allUserData = await state.get_data() # загружаем статусы пользователя
    test2 = allUserData['test']
    userID = allUserData['userID']
    bot_mes_ID = allUserData['bot_mes']
    for i in test2:
        print('-----------' + str(i))
        await bot.delete_message(userID, i)
    for i in bot_mes_ID:
        print('============' + str(i))
        await bot.delete_message(userID, i)
        # await bot.delete_sticker_from_set

    await message.delete()
    await InItStateUser(message, state)
    

@dp.message_handler(commands=['start'])
async def start(message: types.Message, state: FSMContext):
    await message.answer('это просто старт')
    await InItStateUser(message, state)
    allUserData = await state.get_data() # загружаем статусы пользователя
    userID = str(allUserData['userID'])
    test = str(allUserData['test'])
    print(userID)
    print(test)


@dp.message_handler(content_types=['photo'])
@dp.message_handler(content_types=['sticker'])
@dp.message_handler()
async def start(message: types.Message, state: FSMContext):
    """
    Отвечает на ВСЁ.
    А именно на текстовые, фото и стикеры. Запоминает их id.
    """
    mess_id = message.message_id
    bot_answer = await message.answer('ответ на всё')
    bot_answer_id = bot_answer.message_id


    print('mess_id: ' + str(mess_id))
    print('bot_answer_id: ' + str(bot_answer_id))

    allUserData = await state.get_data() # загружаем статусы пользователя 
    test2 = allUserData['test']
    bot_mes2 = allUserData['bot_mes']
    test2.append(mess_id)
    bot_mes2.append(bot_answer_id)
    await state.update_data(test=test2)
    await state.update_data(bot_mes=bot_mes2)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)