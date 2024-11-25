import asyncio
from aiogram import Bot, Dispatcher
from config import *
from StopSpamMidleware import StopSpamMiddleware
from config import get_tg_api_token

#Импорт модулей бота
from standart_questions import main_standart
from other import other_main


async def main():
    bot = Bot(token=get_tg_api_token())

    dp = Dispatcher()

    dp.include_routers(other_main.router, main_standart.router)
    
    dp.callback_query.outer_middleware(StopSpamMiddleware())
    dp.message.outer_middleware(StopSpamMiddleware())
    
    await dp.start_polling(bot)



if __name__ == "__main__":
    asyncio.run(main())