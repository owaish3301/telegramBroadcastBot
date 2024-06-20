from aiogram import Bot
import os
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("TOKEN")

bot = Bot(TOKEN)


async def send_contents(contents, chat_id):
    try:
        for content in contents:
            if content['content_type'] == 'Text':
                await bot.send_message(chat_id, content['caption'])
            elif content['content_type'] == 'Photo':
                await bot.send_photo(chat_id, content['photo'], caption=content['caption'])
            elif content['content_type'] == 'Video':
                await bot.send_video(chat_id, content['video'], caption=content['caption'])
    except Exception as e:
        print("error occured while handling buttons 1 2 or 3, error is :", e)