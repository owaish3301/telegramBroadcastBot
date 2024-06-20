from aiogram import Router, F, Bot
from aiogram.types import Message
from utils.database import DBHelper
from utils.menu_buttons import button1, button2, button3, button4, button5, button6, button7, button8, button9, keyboard, admin_keyboard
from utils.state_manager import StateManager
from utils.send_contents import send_contents
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split()))
TOKEN = os.getenv("TOKEN")
router = Router()
bot = Bot(TOKEN)


@router.message(F.text.in_({button1, button2, button3, button4, button5, button6, button7, button8, button9}))
async def handle_button_click(message: Message):
    user_id = message.from_user.id
    username = message.from_user.username
    first_name = message.from_user.first_name

    state = StateManager.get_instance()
    db = DBHelper(MONGO_URI)
    if not db.user_exists(user_id):
        db.add_user(user_id, username, first_name)

    action = message.text
    if action == button1:
        contents = db.get_button1_content()
        await send_contents(contents, message.chat.id)

    elif action == button2:
        contents = db.get_button2_content()
        await send_contents(contents, message.chat.id)

    elif action == button3:
        contents = db.get_button3_content()
        await send_contents(contents, message.chat.id)

    elif action == button4:
        contents = db.get_button4_content()
        await send_contents(contents, message.chat.id)
    
    elif action == button5 and user_id in ADMIN_IDS:
        state.is_adding_content_to_button_name = "button4"
        state.is_adding_content = True
        state.is_forwarding = False
        await message.answer("Please send the content you want to add for button4.")
    
    elif action == button6 and user_id in ADMIN_IDS:
        state.is_adding_content_to_button_name = "button3"
        state.is_adding_content = True
        state.is_forwarding = False
        await message.answer("Please send the content you want to add for button3.")

    elif action == button7 and user_id in ADMIN_IDS:
        state.is_adding_content_to_button_name = "button2"
        state.is_adding_content = True
        state.is_forwarding = False
        await message.answer("Please send the content you want to add for button2.")

    elif action == button8 and user_id in ADMIN_IDS:
        state.is_adding_content_to_button_name = "button1"
        state.is_adding_content = True
        state.is_forwarding = False
        await message.answer("Please send the content you want to add for button1.")

    elif action == button9 and user_id in ADMIN_IDS:
        state.is_adding_content_to_button_name = "welcome"
        state.is_adding_content = True
        state.is_forwarding = False
        await message.answer("Please send the content you want to add for welcome message.")
