from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from dotenv import load_dotenv
import os
load_dotenv()


WELCOME_MESSAGE_CAPTION = "✅😍 JOIN OUR NEW CHANNELS 🤩✅"


chnl_link_1 = os.getenv("chnl_link_1")
chnl_link_2 = os.getenv("chnl_link_2")
chnl_link_3 = os.getenv("chnl_link_3")
chnl_link_4 = os.getenv("chnl_link_4")

welcom_btn_1 = InlineKeyboardButton(text="👉DESI MMS👈", url=chnl_link_1)
welcom_btn_2 = InlineKeyboardButton(text="LEAKED VIDEOS 🔞", url=chnl_link_2)
welcom_btn_3 = InlineKeyboardButton(text="🥵COLLEGE GIRLS VIDEOS🥵", url=chnl_link_3)
welcom_btn_4 = InlineKeyboardButton(text="DIRECT VIDEOS 😉", url=chnl_link_4)
inline_btn = InlineKeyboardMarkup(inline_keyboard=[[welcom_btn_1], [welcom_btn_2], [welcom_btn_3], [welcom_btn_4]])
