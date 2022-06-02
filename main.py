import telebot
import config

from Keyboards import keyboard_yesno, keyboard_delete, keyboard_select_quiz, keyboard_ok
from UserInformation import *
from FilmsList import *
from Texts import *

bot = telebot.TeleBot(config.token)

temp_film = 0
base = Base()

@bot.message_handler(content_types=['text'])
def start(message):
    global base
    base = Base()

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
    if message.text == 'Да':
        bot.send_message(message.from_user.id, "Тогда перепроверь и введи снова")
        bot.register_next_step_handler(message, check_nick)
    else:
        bot.send_message(message.from_user.id, "Тогда создай пользователя", reply_markup=keyboard_delete)
        bot.register_next_step_handler(message, get_nick)


@bot.message_handler(content_types=['text'])
def check_nick(message):
    entered_nick = message.text
    founded_id = base.check_in_base(entered_nick)
    if founded_id != -1:
        base.change_user_name(entered_nick)
        question = "И снова здравствуйте,во что играем?"
        bot.send_message(message.from_user.id, question, reply_markup=keyboard_select_quiz)
        bot.register_next_step_handler(message, first_game)
    else:
        question = "Ты точно существуешь?"
        bot.send_message(message.from_user.id, question, reply_markup=keyboard_yesno)
        bot.register_next_step_handler(message, yesno_help_function)


@bot.message_handler(content_types=['text'])
def get_nick(message):
    base.push_new_user(message.text)
    bot.send_message(message.from_user.id, 'Введи возраст')
    bot.register_next_step_handler(message, get_age)


def generations_answer(mess, t):
    return (bot.send_message(mess.from_user.id,
                             "Категорически приветствую, " + t + ", а теперь выбирай игру:",
                             reply_markup=keyboard_select_quiz))

@bot.message_handler(content_types=['text'])
def get_age(message):
    try:
        age = int(message.text)
    except ValueError:
        bot.send_message(message.from_user.id, 'Возраст - это число')
        bot.register_next_step_handler(message, get_age)
        return

    if age < 18:
        generations_answer(message, "Школьник")
    elif age > 40:
        generations_answer(message, "Динозавр")
    else:
        generations_answer(message, base.get_user_name())

    bot.register_next_step_handler(message, first_game)

@bot.message_handler(content_types=['text'])
def first_game(message):
    if message.text == "Фильмы":
        if base.get_unused_film() == -1:
            bot.send_message(message.from_user.id, "Ты прошел игру!")
            return

        bot.send_message(message.from_user.id, film_intro,
                         reply_markup=keyboard_ok)
        bot.register_next_step_handler(message, one_round_film_game)
    else:
        bot.send_message(message.from_user.id, "Ты как это сделал?")
        bot.register_next_step_handler(message, first_game)


@bot.message_handler(content_types=['text'])
def not_first_film_game(message):
    if message.text == "Да":
        if base.get_unused_film() == -1:
            bot.send_message(message.from_user.id, "Ты прошел игру!")
            return

        bot.send_message(message.from_user.id, "Поехали")
        bot.register_next_step_handler(message, one_round_film_game)
    else:
        bot.send_message(message.from_user.id, "Пока")


@bot.message_handler(content_types=['text'])
def one_round_film_game(message):

    if base.answer_is_right(message.text):
        base.update()
        question = "Правильно! Продолжаем?"
        bot.send_message(message.from_user.id, question, reply_markup=keyboard_yesno)
        bot.register_next_step_handler(message, not_first_film_game)
    else:
        base.change_que_number()
        if base.still_in_game():
            question = "Ты проиграл( Начать снова?"
            bot.send_message(message.from_user.id, question, reply_markup=keyboard_yesno)
            bot.register_next_step_handler(message, not_first_film_game)
        question = base.new_task()
        bot.send_message(message.from_user.id, question)
        bot.register_next_step_handler(message, one_round_film_game)
        return


bot.polling(none_stop=True, interval=0)
