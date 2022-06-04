import telebot
import config

from Keyboards import keyboard_yesno, keyboard_delete, keyboard_select_quiz, keyboard_ok
from UserInformation import *
from Texts import *

bot = telebot.TeleBot(config.token)

base = {}


@bot.message_handler(content_types=['text'])
def start(message):

    """
    Main function that targets to other and start creating of user


    :param message: message from user
    :return: goes to other functions of bot, may show table of results
    """

    global base
    base[message.from_user.id] = Base()
    temp = base[message.from_user.id]

    if message.text == '/reg':
        bot.send_message(message.from_user.id, "Придумай какой-нибудь ник для себя")
        bot.register_next_step_handler(message, get_nick)
    elif message.text == '/sig':
        bot.send_message(message.from_user.id, "Введи свой ник")
        bot.register_next_step_handler(message, check_nick)
    elif message.text == '/res':
        diction = temp.get_results()
        base[message.from_user.id] = temp
        bot.send_message(message.from_user.id, diction)
    else:
        bot.send_message(message.from_user.id, 'Напиши /reg , если новенький'
                                               ' /sig , если уже смешарик'
                                               ' /res , если хочешь посмотреть общие результаты')


@bot.message_handler(content_types=['text'])
def yesno_help_function(message):

    """
    Asks user if he really exists

    :param message: message from user (Да или нет)
    :return: goes to another bot function if nick exists or no
    """

    if message.text == 'Да':
        bot.send_message(message.from_user.id, "Тогда перепроверь и введи снова")
        bot.register_next_step_handler(message, check_nick)
    else:
        bot.send_message(message.from_user.id, "Тогда создай пользователя", reply_markup=keyboard_delete)
        bot.register_next_step_handler(message, get_nick)


@bot.message_handler(content_types=['text'])
def check_nick(message):

    """Check existing of user

    :param message: message from user
    :return: goes to the game when nick is correct
    """

    temp = base[message.from_user.id]
    entered_nick = message.text
    founded_id = temp.existion(entered_nick)
    if founded_id != -1:
        temp.set_user_id(entered_nick)
        base[message.from_user.id] = temp
        question = "И снова здравствуйте,во что играем?"
        bot.send_message(message.from_user.id, question, reply_markup=keyboard_select_quiz)

        bot.register_next_step_handler(message, first_game)
    else:
        question = "Ты точно существуешь?"
        bot.send_message(message.from_user.id, question, reply_markup=keyboard_yesno)
        bot.register_next_step_handler(message, yesno_help_function)


@bot.message_handler(content_types=['text'])
def get_nick(message):

    """
    Get nick from user and creates user

    :param message: message from user
    :return: goes to stage of getting age
    """

    temp = base[message.from_user.id]
    temp.push_new_user(message.text)
    base[message.from_user.id] = temp

    bot.send_message(message.from_user.id, 'Введи возраст')
    bot.register_next_step_handler(message, get_age)


def generations_answer(mess, t):
    """
    Generates easter agg depends on the age of user

    :param mess: message from user
    :param t: user generation
    :return: generated string
    """

    return (bot.send_message(mess.from_user.id,
                             "Категорически приветствую, " + t + ", а теперь выбирай игру:",
                             reply_markup=keyboard_select_quiz))


@bot.message_handler(content_types=['text'])
def get_age(message):

    """
    Get age of user needed in joke purpose

    :param message: message from user
    :return: starts game
    """

    temp = base[message.from_user.id]
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
        generations_answer(message, temp.get_user_name())

    base[message.from_user.id] = temp
    bot.register_next_step_handler(message, first_game)


@bot.message_handler(content_types=['text'])
def first_game(message):

    """
    Generates film for this user at first time

    :param message: message from user
    :return:
    """

    temp = base[message.from_user.id]
    if message.text == "Фильмы":
        if temp.get_unused_film() == -1:
            bot.send_message(message.from_user.id, "Что-то пошло не так!")
            return

        bot.send_message(message.from_user.id, film_intro,
                         reply_markup=keyboard_ok)
        bot.register_next_step_handler(message, one_round_film_game)
    else:
        bot.send_message(message.from_user.id, "Ты как это сделал?")
        bot.register_next_step_handler(message, first_game)


@bot.message_handler(content_types=['text'])
def not_first_film_game(message):

    """
    Generates film for this user not at first time

    :param message: message from user
    :return:
    """

    temp = base[message.from_user.id]
    if message.text == "Да":
        if temp.get_unused_film() == -1:
            bot.send_message(message.from_user.id, "Ты прошел игру!")
            bot.register_next_step_handler(message, start)
            return

        bot.send_message(message.from_user.id, "Поехали, помни, что некоторые подсказки нужно подождать",
                         reply_markup=keyboard_ok)
        bot.register_next_step_handler(message, one_round_film_game)
    else:
        bot.send_message(message.from_user.id, "Пока")


@bot.message_handler(content_types=['text'])
def one_round_film_game(message):

    """
    Checks if user answer is right
    After that asks user about film and gets answer

    :param message: message from user
    :return: goes to the next round, next game or stop session
    """

    temp = base[message.from_user.id]
    if temp.answer_is_right(message.text) == config.please_stop:
        bot.send_message(message.from_user.id, temp.answer_is_right(message.text), reply_markup=keyboard_delete)

    if temp.answer_is_right(message.text):
        temp.update()
        base[message.from_user.id] = temp

        question = "Правильно! Продолжаем?"
        bot.send_message(message.from_user.id, question, reply_markup=keyboard_yesno)
        bot.register_next_step_handler(message, not_first_film_game)
    else:
        if not temp.full_questions():
            bot.send_message(message.from_user.id, "Мимо", reply_markup=keyboard_delete)

        temp.change_que_number()
        base[message.from_user.id] = temp
        if temp.still_in_game():
            question = "Ты проиграл( \n Ответ:  " + temp.final_answer() + "\nНачать снова?"
            bot.send_message(message.from_user.id, question, reply_markup=keyboard_yesno)
            bot.register_next_step_handler(message, not_first_film_game)
            return

        question = temp.new_task()
        if question[0] == if_foto:
            img = open(question[1], 'rb')
            bot.send_photo(message.from_user.id, img)
        else:
            bot.send_message(message.from_user.id, question[1])
        bot.register_next_step_handler(message, one_round_film_game)


bot.polling(none_stop=True, interval=0)
