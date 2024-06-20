from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

button1 = 'Premium videos 🍑'
button2 = 'New Videos 🥵'
button3 = 'Viral Videos 🔞'
button4 = 'Terabox Videos 😉'
button5 = 'Add content to button4'  
button6 = 'Add content to button3'
button7 = 'Add content to button2'
button8 = 'Add content to button1'
button9 = 'Add content to welcome button'

menu_buttons = [
    [KeyboardButton(text=button1)],
    [KeyboardButton(text=button2)],
    [KeyboardButton(text=button3), KeyboardButton(text=button4)],
]
keyboard = ReplyKeyboardMarkup(keyboard=menu_buttons, is_persistent=True, resize_keyboard=True)

admin_menu_buttons = [
    [KeyboardButton(text=button1)],
    [KeyboardButton(text=button2)],
    [KeyboardButton(text=button3), KeyboardButton(text=button4)],
    [KeyboardButton(text=button9)],
    [KeyboardButton(text=button8)],
    [KeyboardButton(text=button7)],
    [KeyboardButton(text=button6)],
    [KeyboardButton(text=button5)]
]
admin_keyboard = ReplyKeyboardMarkup(keyboard=admin_menu_buttons, is_persistent=True, resize_keyboard=True)
