from telebot.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_yes = KeyboardButton("Да")
button_no = KeyboardButton("Нет")

keyboard_yesno = ReplyKeyboardMarkup(resize_keyboard=True).row(button_yes, button_no)

keyboard_delete = ReplyKeyboardRemove()