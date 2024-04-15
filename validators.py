from config import config
from database import count_all_symbol


def is_tts_symbol_limit(message):
    user_id = message.from_user.id
    text_symbols = len(message.text)

    all_symbols = count_all_symbol(user_id) + text_symbols

    if all_symbols >= int(config['LIMITS']['MAX_TTS_SYMBOLS']):
        msg = (f"Превышен общий лимит SpeechKit TTS {config['LIMITS']['MAX_TTS_SYMBOLS']}. Использовано: "
               f"{all_symbols} символов. Доступно: {int(config['LIMITS']['MAX_TTS_SYMBOLS']) - all_symbols}")
        return False, msg

    if text_symbols >= int(config['LIMITS']['MAX_USER_TTS_SYMBOLS']):
        msg = f"Превышен лимит SpeechKit TTS на запрос {config['LIMITS']['MAX_USER_TTS_SYMBOLS']}, в сообщении {text_symbols} символов"
        return False, msg

    return len(message.text), 'Ваш запрос соответствует количеству символов'


# def is_digit(message):
#     if message.isdigit():
#         return True
#     else:
#         return False
