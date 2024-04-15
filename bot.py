import logging
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from database import limit_users, check_user_in_db, create_table, insert_data, count_all_symbol
from config import config, bot_token
from validators import is_tts_symbol_limit

bot = telebot.TeleBot(token=bot_token)


@bot.message_handler(commands=['start'])
def say_start(message):
    bot.send_message(message.chat.id, f'hello!!!!!!!!!!!!')
    create_table()

    user_id = message.from_user.id
    limit = limit_users()
    checked_user = check_user_in_db(user_id)

    if limit and not checked_user:
        bot.send_message(message.chat.id, f'limit!!!!!!!!!!!!')
    else:
        insert_data(user_id)
        bot.send_message(message.chat.id, f'Для генерации напишите /tts')


@bot.message_handler(commands=['help'])
def say_help(message):
    bot.send_message(message.chat.id, f'help!!!!!!!!!!!!')


@bot.message_handler(commands=['tts'])
def tts_handler(message):
    user_id = message.from_user.id
    checked_user = check_user_in_db(user_id)
    if checked_user:
        bot.send_message(message.chat.id, f"Введите текст для генерации")
        bot.register_next_step_handler(message, text_to_speech)
    else:
        bot.send_message(message.chat.id, 'LIMITTTTTT!!!!!!!!')


def text_to_speech(message):
    user_id = message.from_user.id

    if message.text.isdigit():
        bot.send_message(message.chat.id, 'Вветите текст, а не число!!')

    else:
        symbols, msg = is_tts_symbol_limit(message)

        if not symbols:
            bot.send_message(message.chat.id, msg)

        else:
            print(message.text)

            insert_data(user_id, message.text, symbols)

    bot.register_next_step_handler(message, text_to_speech)


@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)
        logging.info("Use command DEBUG")


bot.polling()
