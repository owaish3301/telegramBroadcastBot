import asyncio
import logging
from aiogram import Bot, Dispatcher
from handlers import start_router, broadcast_router, commands_router, messages_router, chat_join_request_router
from utils.logging import MyRequestLogging

import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split()))

bot = Bot(TOKEN)
dp = Dispatcher()

# Custom RequestLogging middleware
bot.session.middleware(MyRequestLogging(ignore_methods=['getUpdates']))

async def main() -> None:
    dp.include_router(start_router)
    dp.include_router(broadcast_router)
    dp.include_router(commands_router)
    dp.include_router(messages_router)
    dp.include_router(chat_join_request_router)

    # Pass the bot instance to the broadcast router
    broadcast_router.bot_instance = bot

    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    asyncio.run(main())
