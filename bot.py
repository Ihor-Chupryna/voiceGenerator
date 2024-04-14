import logging
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from database import limit_users, check_user_in_db, create_table, insert_data
from config import config, bot_token


bot = telebot.TeleBot(token=bot_token)

users = {}


def create_buttons(list_buttons: list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for button in list_buttons:
        keyboard.add(KeyboardButton(button))

    return keyboard


@bot.message_handler(commands=['start'])
def say_start(message):
    bot.send_message(message.chat.id, f'hello!!!!!!!!!!!!')

    create_table()
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    limit = limit_users()
    checked_user = check_user_in_db(user_id)
    if limit and not checked_user:
        bot.send_message(message.chat.id, f'limit!!!!!!!!!!!!')
    else:
        insert_data(user_id, user_name)
        bot.send_message(message.chat.id, f'Для генерации напишите /tts')


@bot.message_handler(commands=['help'])
def say_help(message):
    bot.send_message(message.chat.id, f'help!!!!!!!!!!!!')


@bot.message_handler(commands=['tts'])
def text_to_speech(message):
    user_id = message.from_user.id
    checked_user = check_user_in_db(user_id)
    if checked_user:
        users[user_id] = {
            'tts_symbols': ''
        }
        bot.send_message(message.chat.id, f"Введите текст для генерации")
        bot.register_next_step_handler(message, tts_handler)
    else:
        bot.send_message(message.chat.id, 'LIMITTTTTT!!!!!!!!')


def tts_handler(message):
    print(message.text)


@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)
        logging.info("Use command DEBUG")


bot.polling()
