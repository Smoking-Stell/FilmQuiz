import telebot
import csv

bot = telebot.TeleBot('5160953743:AAEiEMtJR-59wS7PuTD8N_AslzCsH452Veg')


@bot.message_handler(content_types=['text'])
def game(message):
    bot.send_message(message.from_user.id, "Хуй")