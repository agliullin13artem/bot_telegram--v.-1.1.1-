import asyncio
import os
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart
from aiogram.enums.parse_mode import ParseMode
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties


# импортируем функцию для поиска .env
from dotenv import find_dotenv, load_dotenv
# загружаем переменные окружения
load_dotenv(find_dotenv()) 


from handlers.user_private import user_private_router
from handlers.user_group import user_group_router
from common.bot_cmds_list import private

# доступные типы обновлений
ALLOWED_UPDATES = ['message', 'edited_message']

# бот токен из переменных окружения и парсмод html 
bot = Bot(token = os.getenv("TOKEN"), default=DefaultBotProperties(parse_mode=ParseMode.HTML))

# диспетчер
dp = Dispatcher() # диспетчер бота

# включаем роутер
dp.include_router(user_private_router) 
dp.include_router(user_group_router)

# асинхронный метод для запуска бота
async def main():
    await bot.delete_webhook(drop_pending_updates=True) # удаляем старый хук
    # await bot.delete_my_commands(scope=types.BotCommandScopeAllPrivateChats()) # удаляем старые команды
    await bot.set_my_commands(commands=private, scope=types.BotCommandScopeAllPrivateChats()) # устанавливаем команд
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES) # запускаем бота


# вызываем функцию маин
asyncio.run(main())