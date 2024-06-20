import logging
from aiogram import Router
from utils.inline_buttons import inline_btn, WELCOME_MESSAGE_CAPTION
from aiogram.types import ChatJoinRequest
from utils.database import DBHelper
from utils.send_contents import send_contents
from utils.menu_buttons import keyboard
import os
from dotenv import load_dotenv

load_dotenv()

router = Router()
db = DBHelper(os.getenv("MONGO_URI"))

@router.chat_join_request()
async def chat_join_request(update: ChatJoinRequest):
    await update.bot.send_message(chat_id=update.from_user.id, text="laoding...", reply_markup=keyboard)

    contents = db.get_welcome_content()
    try:
        await send_contents(contents, update.from_user.id)
        await update.bot.send_message(chat_id=update.from_user.id, text=WELCOME_MESSAGE_CAPTION, reply_markup=inline_btn)

        await update.approve()
    except Exception as e:
        logging.error(f"Error occurred during chat_join_request: {e}")
