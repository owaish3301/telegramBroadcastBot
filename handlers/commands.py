from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from utils.database import DBHelper
import os
from dotenv import load_dotenv
import logging
from utils.state_manager import StateManager

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split()))

router = Router()

@router.message(Command('subscribers'), F.from_user.id.in_(ADMIN_IDS))
async def subscriber_count(message: Message):
    try:
        db = DBHelper(MONGO_URI)
        active_user_count = db.users.count_documents({})
        blocked_user_count = db.blocked_users.count_documents({})
        total_user_count = active_user_count + blocked_user_count

        report_text = f"Active Users: {active_user_count}\n" \
                      f"Blocked Users: {blocked_user_count}\n" \
                      f"Total Users: {total_user_count}"
        await message.answer(report_text)
    except Exception as e:
        logging.error(f"Error occurred during subscriber_count: {e}")

@router.message(Command("stop_all"), F.from_user.id.in_(ADMIN_IDS))
async def stopAll(message:Message):
    await message.answer("turned all switch to false")
    state = StateManager.get_instance()
    state.is_forwarding = False
    state.is_adding_content = False