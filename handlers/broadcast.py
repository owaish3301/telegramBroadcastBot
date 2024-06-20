from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
import asyncio
import logging
import re
from utils.database import DBHelper
from utils.menu_buttons import button1, button2, button3, button4, button5, button6, button7, button8, button9
from utils.state_manager import StateManager
import os
from dotenv import load_dotenv

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
ADMIN_IDS = list(map(int, os.getenv("ADMIN_IDS").split()))

router = Router()
router.bot_instance = None  # Placeholder for the bot instance

message_queue = []

@router.message(Command('start_broadcast'), F.from_user.id.in_(ADMIN_IDS))
async def start_broadcast(message: Message):
    state = StateManager.get_instance()
    state.is_forwarding = True
    state.is_adding_content = False
    await message.answer("Broadcast forwarding mode enabled. Send messages to be forwarded.")

@router.message(Command('stop_broadcast'), F.from_user.id.in_(ADMIN_IDS))
async def stop_broadcast(message: Message):
    state = StateManager.get_instance()
    state.is_forwarding = False
    message_queue.clear()
    await message.answer("Broadcast forwarding mode disabled.")

@router.message(Command('broadcast'), F.from_user.id.in_(ADMIN_IDS))
async def broadcast(message: Message):
    await message.answer("Messages queued for broadcasting.")
    await asyncio.create_task(broadcast_messages())
    await message.answer("Broadcasting completed.")

@router.message(F.from_user.id.in_(ADMIN_IDS), ~F.text.in_({button1, button2, button3, button4, button5, button6, button7, button8, button9, "/subscribers", "/stop_all"}))
async def handle_messages(message: Message):
    state = StateManager.get_instance()
    if state.is_forwarding:
        message_data = create_message_data(message)
        message_queue.append(message_data)
    elif state.is_adding_content:
        await add_content(message, state.is_adding_content_to_button_name)

def create_message_data(message: Message):
    message_data = {'id': message.message_id, 'type': '', 'text': message.text, 'photo': '', 'video': '', 'caption': ''}
    if message.text:
        message_data['type'] = 'Text'
    elif message.photo:
        message_data['type'] = 'Photo'
        message_data['photo'] = message.photo[-1].file_id
        message_data['caption'] = message.caption or ""
    elif message.video:
        message_data['type'] = 'Video'
        message_data['video'] = message.video.file_id
        message_data['caption'] = message.caption
    return message_data

async def add_content(message: Message, button_name: str):
    db = DBHelper(MONGO_URI)
    content_type, caption, photo, video = extract_content(message)
    if button_name == "button4":
        db.add_button4_content(message.from_user.id, content_type, caption, photo, video)
        await message.answer("Content added for Button4.")
    elif button_name == "button3":
        db.add_button3_content(message.from_user.id, content_type, caption, photo, video)
        await message.answer("Content added for Button3.")
    elif button_name == "button2":
        db.add_button2_content(message.from_user.id, content_type, caption, photo, video)
        await message.answer("Content added for Button2.")
    elif button_name == "button1":
        db.add_button1_content(message.from_user.id, content_type, caption, photo, video)
        await message.answer("Content added for Button1.")
    elif button_name == "welcome":
        db.add_welcome_content(message.from_user.id, content_type, caption, photo, video)
        await message.answer("content added for welcome message")


def extract_content(message: Message):
    content_type, caption, photo, video = '', '', '', ''
    if message.text:
        content_type = 'Text'
        caption = message.text
    elif message.photo:
        content_type = 'Photo'
        photo = message.photo[-1].file_id
        caption = message.caption
    elif message.video:
        content_type = 'Video'
        video = message.video.file_id
        caption = message.caption
    return content_type, caption, photo, video



async def broadcast_messages():
    global message_queue
    db = DBHelper(MONGO_URI)
    subscribers = db.get_all_subscribers()
    total_subscribers = len(subscribers)
    progress_message = await router.bot_instance.send_message(chat_id=ADMIN_IDS[0], text="Broadcasting in progress...")
    
    for current_subscriber, subscriber_id in enumerate(subscribers, start=1):
        await update_progress(progress_message, current_subscriber, total_subscribers)
        await send_messages_to_subscriber(subscriber_id)
        
    message_queue.clear()

async def update_progress(progress_message: Message, current_subscriber: int, total_subscribers: int):
    progress = current_subscriber / total_subscribers
    progress_text = f"Progress: [{('=' * int(progress * 20)).ljust(20)}] {progress * 100:.2f}%\nUsers received: {current_subscriber}/{total_subscribers}"
    await router.bot_instance.edit_message_text(chat_id=progress_message.chat.id, message_id=progress_message.message_id, text=progress_text)

async def send_messages_to_subscriber(subscriber_id: int):
    for message_data in message_queue:
        try:
            if message_data['type'] == 'Text':
                await router.bot_instance.send_message(chat_id=subscriber_id, text=message_data['text'])
            elif message_data['type'] == 'Photo':
                await router.bot_instance.send_photo(chat_id=subscriber_id, photo=message_data['photo'], caption=message_data['caption'])
            elif message_data['type'] == 'Video':
                await router.bot_instance.send_video(chat_id=subscriber_id, video=message_data['video'], caption=message_data['caption'])
        except Exception as e:
            handle_broadcast_exception(e, subscriber_id)


def handle_broadcast_exception(exception, subscriber_id):
    db = DBHelper(MONGO_URI)
    if re.search(r'bot was blocked by the user', str(exception)):
        logging.error(f"{exception}")
        db.move_user_to_blocked_table(subscriber_id)
    else:
        print("error while sending messages")
        logging.error(f"{exception}")

