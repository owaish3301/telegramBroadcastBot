from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from utils.database import DBHelper
from utils.inline_buttons import WELCOME_MESSAGE_CAPTION, inline_btn
from utils.menu_buttons import keyboard, admin_keyboard
from utils.send_contents import send_contents

import os
from dotenv import load_dotenv
import logging

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split()))

router = Router()

@router.message(CommandStart())
async def start_function(msg: Message) -> None:
    try:
        await msg.answer(text = "loading...", reply_markup=keyboard)
        user_id = msg.from_user.id
        username = msg.from_user.username
        first_name = msg.from_user.first_name

        db = DBHelper(MONGO_URI)
        db.add_user(user_id, username, first_name)

        content = db.get_welcome_content()
        await send_contents(content, msg.chat.id)

        if user_id in ADMIN_IDS:
            await msg.answer(text="hello admin", reply_markup = admin_keyboard)
            await msg.answer(text=WELCOME_MESSAGE_CAPTION, reply_markup = inline_btn)
        else:
            await msg.answer(text=WELCOME_MESSAGE_CAPTION, reply_markup = inline_btn)
    except Exception as e:
        logging.error(f"Error occurred during start_function: {e}")
