from telebot.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_yes = KeyboardButton("Да")
button_no = KeyboardButton("Нет")

keyboard_yesno = ReplyKeyboardMarkup(resize_keyboard=True).row(button_yes, button_no)

keyboard_delete = ReplyKeyboardRemove()

button_film = KeyboardButton("Фильмы")

keyboard_select_quiz = ReplyKeyboardMarkup(resize_keyboard=True).row(button_film, button_film)

button_ok = KeyboardButton("Ok")

keyboard_ok = ReplyKeyboardMarkup(resize_keyboard=True).row(button_ok)