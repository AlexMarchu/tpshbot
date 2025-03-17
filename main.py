from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

import os
import asyncio

from handlers import router

load_dotenv()

bot = Bot(token=os.getenv("BOT_TOKEN"))
dp = Dispatcher()
dp.include_router(router)


async def main():
    print("🟢 Bot started")
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🔴 Bot stopped")
