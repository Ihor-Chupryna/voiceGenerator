import logging
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from database import limit_users, check_user_in_db, create_table, insert_data, count_all_symbol
from config import config, bot_token
# from validators import is_tts_symbol_limit


bot = telebot.TeleBot(token=bot_token)

users = {}


def create_buttons(list_buttons: list):
    keyboard = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    for button in list_buttons:
        keyboard.add(KeyboardButton(button))

    return keyboard


def is_tts_symbol_limit(message):
    user_id = message.from_user.id
    text_symbols = len(message.text)

    # Функция из БД для подсчёта всех потраченных пользователем символов
    all_symbols = count_all_symbol(user_id) + text_symbols

    # Сравниваем all_symbols с количеством доступных пользователю символов
    if all_symbols >= int(config['LIMITS']['MAX_TTS_SYMBOLS']):
        msg = (f"Превышен общий лимит SpeechKit TTS {config['LIMITS']['MAX_TTS_SYMBOLS']}. Использовано: "
               f"{all_symbols} символов. Доступно: {int(config['LIMITS']['MAX_TTS_SYMBOLS']) - all_symbols}")
        bot.send_message(user_id, msg)
        return None

    # Сравниваем количество символов в тексте с максимальным количеством символов в тексте
    if text_symbols >= int(config['LIMITS']['MAX_USER_TTS_SYMBOLS']):
        msg = f"Превышен лимит SpeechKit TTS на запрос {config['LIMITS']['MAX_USER_TTS_SYMBOLS']}, в сообщении {text_symbols} символов"
        bot.send_message(user_id, msg)
        return None
    return len(message.text)


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
        users[user_id] = {
            'tts_symbols': ''
        }
        bot.send_message(message.chat.id, f"Введите текст для генерации")
        bot.register_next_step_handler(message, text_to_speech)
    else:
        bot.send_message(message.chat.id, 'LIMITTTTTT!!!!!!!!')


def text_to_speech(message):
    user_id = message.from_user.id
    print(message.text)

    symbols = is_tts_symbol_limit(message)
    insert_data(user_id, message.text, symbols)
    print('===================================')
    print(symbols)
    bot.register_next_step_handler(message, text_to_speech)


@bot.message_handler(commands=['debug'])
def send_logs(message):
    with open("log_file.txt", "rb") as f:
        bot.send_document(message.chat.id, f)
        logging.info("Use command DEBUG")


bot.polling()
