from telebot.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

button_yes = KeyboardButton("Да")
button_no = KeyboardButton("Нет")

keyboard_yesno = ReplyKeyboardMarkup(resize_keyboard=True).row(button_yes, button_no)

keyboard_delete = ReplyKeyboardRemove()

button_film1 = KeyboardButton("Фильмы")
button_film2 = KeyboardButton("Кинематограф")

keyboard_select_quiz = ReplyKeyboardMarkup(resize_keyboard=True).row(button_film1, button_film1)

button_ok = KeyboardButton("Ok")

keyboard_ok = ReplyKeyboardMarkup(resize_keyboard=True).row(button_ok)