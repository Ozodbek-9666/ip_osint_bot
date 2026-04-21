import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from bot_handlres import router # Router'ni import qilamiz
from database import init_db
load_dotenv()

async def main():
    init_db() # Bazani yaratish
    await dp.start_polling(bot)
    bot = Bot(token=os.getenv("BOT_TOKEN"))
    dp = Dispatcher()
    
    # Routerni ulash
    dp.include_router(router)
    
    print("Bot ishga tushdi...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())