from functools import reduce
import psycopg2, config
from aiogram import Bot

bot = Bot(token=config.BOT_TOKEN)

def reg (chat_id: int):
    conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD, host=config.DB_HOST)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"SELECT COUNT (*) FROM members WHERE chat_id={chat_id}")
    check = reduce(lambda rst, d: rst * 10 + d, cursor.fetchone())
    if check == 1:
        cursor.close()
        conn.close()
    else:
        mas = (chat_id, '')
        cursor.execute(f"INSERT INTO members (chat_id, questions) VALUES {mas}")
        cursor.close()
        conn.close()
    return

def get_users():
    conn = psycopg2.connect(dbname=config.DB_NAME, user=config.DB_USER, password=config.DB_PASSWORD, host=config.DB_HOST)
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute(f"SELECT chat_id FROM members")
    users_list = [item[0] for item in cursor.fetchall()]
    return users_list