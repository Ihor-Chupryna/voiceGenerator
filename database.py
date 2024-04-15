import logging
import sqlite3
from config import config


def create_table():
    try:
        con = sqlite3.connect('speech_kit.db')
        cur = con.cursor()
        cur.execute('''
            CREATE TABLE IF NOT EXISTS messages(
            id INTEGER PRIMARY KEY,
            user_id INTEGER,
            text TEXT,
            tts_symbols INTEGER);
        ''')
        logging.info('table was created')
    except sqlite3.Error as error:
        logging.error(f'Error database:', error)
    finally:
        con.close()


def limit_users():
    count = 0
    try:
        con = sqlite3.connect('speech_kit.db')
        cur = con.cursor()
        result = cur.execute('SELECT DISTINCT user_id FROM messages')
        for i in result:
            count += 1
    except Exception as error:
        logging.error("Database error", error)
    finally:
        con.close()
        return count >= int(config['LIMITS']['MAX_USERS'])


def check_user_in_db(user_id):
    try:
        con = sqlite3.connect('speech_kit.db')
        cur = con.cursor()
        query = cur.execute('''
                    SELECT user_id
                    FROM messages
                    WHERE user_id = ?
                    LIMIT 1
                ''', (user_id,))
        result = query.fetchall()
        logging.info('get data from database')
        return bool(result)
    except sqlite3.Error as error:
        logging.error('Error database', error)
    finally:
        con.close()


def insert_data(user_id=None, text=None, tts_symbols=0):
    try:
        con = sqlite3.connect('speech_kit.db')
        cur = con.cursor()
        cur.execute(f'INSERT INTO messages(user_id, text, tts_symbols)'
                    f'VALUES (?, ?, ?);',
                    (user_id, text, tts_symbols,))
        logging.info('data is written to the database')
        con.commit()
    except sqlite3.Error as error:
        logging.error(f'Error database:', error)
    finally:
        con.close()


def count_all_symbol(user_id):
    try:
        with sqlite3.connect("speech_kit.db") as con:
            cursor = con.cursor()
            cursor.execute('''SELECT SUM(tts_symbols) FROM messages WHERE user_id=?''', (user_id,))
            data = cursor.fetchone()
            if data and data[0]:
                logging.info('symbols have been counted')
                return data[0]
            else:
                logging.info('symbols column is empty')
                return 0
    except sqlite3.Error as error:
        logging.error(f'Error database:', error)
    finally:
        con.close()