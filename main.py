import asyncio
from aiogram import Bot, Dispatcher
from bot_handlres import router # Routeringizni import qiling
import os
from dotenv import load_dotenv

load_dotenv()

# Bot va Dispatcher ni yaratamiz
bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()

async def main():
    # Routerni Dispatcher-ga ulaymiz
    dp.include_router(router)
    
    print("Bot ishga tushdi...")
    # Pollingni boshlaymiz
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())