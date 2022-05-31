import telebot
import csv

from Keyboards import keyboard_yesno

bot = telebot.TeleBot('5160953743:AAEiEMtJR-59wS7PuTD8N_AslzCsH452Veg')

user_name = ""
user_id = -1
base_of_users = []


def take_base():
    ans = -1
    with open("./base.csv", encoding='utf-8') as r_file:
        file_reader = csv.reader(r_file, delimiter=",")
        for row in file_reader:
            base_of_users.append(row)


def check_in_base(usr):
    for i in range(len(base_of_users)):
        if base_of_users[i][0] == usr:
            return i
    return -1



@bot.message_handler(content_types=['text'])
def start(message):
    take_base()

    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Придумай какой-нибудь ник для себя")
        bot.register_next_step_handler(message, get_nick)
    elif message.text == '/sig':
        bot.send_message(message.from_user.id, "Введи свой ник")
        bot.register_next_step_handler(message, check_nick)
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg , если новенький или /sig , если уже смешарик')


@bot.message_handler(content_types=['text'])
def yesno_help_function(message):
    if message.text == 'Yes':
        bot.send_message(message.from_user.id, "Тогда перепроверь и введи снова")
        bot.register_next_step_handler(message, check_nick)
    else:
        bot.send_message(message.from_user.id, "Тогда создай пользователя")
        bot.register_next_step_handler(message, get_nick)


@bot.message_handler(content_types=['text'])
def check_nick(message):
    global user_name

    entered_nick = message.text
    founded_id = check_in_base(entered_nick)
    if founded_id != -1:
        user_name = entered_nick
        bot.register_next_step_handler(message, game)
    else:
        question = "Ты точно существуешь?"
        bot.send_message(message.from_user.id, text=question, reply_markup=keyboard_yesno)
        bot.register_next_step_handler(message, yesno_help_function)


@bot.message_handler(content_types=['text'])
def get_nick(message):
    global user_name
    user_name = message.text
    bot.send_message(message.from_user.id, 'Введи возраст')
    bot.register_next_step_handler(message, get_age)


@bot.message_handler(content_types=['text'])
def get_age(message):
    age = -1
    while age == -1:
        try:
            age = int(message.text)
        except Exception:
            age = -1
            bot.send_message(message.from_user.id, 'Возраст - это число')
    global user_name
    if age < 18:
        bot.send_message(message.from_user.id, "Категорически приветствую, Школьник")
    elif age > 40:
        bot.send_message(message.from_user.id, "Категорически приветствую, Динозавр")
    else:
        bot.send_message(message.from_user.id, "Категорически приветствую, " + user_name)
    bot.register_next_step_handler(message, game)


@bot.message_handler(content_types=['text'])
def game(message):
    bot.send_message(message.from_user.id, "Хуй")


bot.polling(none_stop=True, interval=0)
