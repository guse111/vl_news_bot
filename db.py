import sqlite3
from datetime import datetime

def init_db():
    conn = sqlite3.connect('news_bot.db')
    c = conn.cursor()

    # Таблица пользователей
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT,
            first_name TEXT,
            last_name TEXT,
            date_joined TEXT
        )
    ''')

    # Таблица новостей
    c.execute('''
        CREATE TABLE IF NOT EXISTS news (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            url TEXT NOT NULL,
            date TEXT NOT NULL,
            text TEXT NOT NULL,
            parsed_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    conn.close()

def add_user(user_id, username, first_name, last_name):
    conn = sqlite3.connect('news_bot.db')
    c = conn.cursor()
    c.execute('''
        INSERT OR IGNORE INTO users (id, username, first_name, last_name, date_joined)
        VALUES (?, ?, ?, ?, ?)
    ''', (user_id, username, first_name, last_name, datetime.now().isoformat()))
    conn.commit()
    conn.close()

def save_news_to_db(title, url, text,  date):
    conn = sqlite3.connect('news_bot.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO news (title, url, text, date)
        VALUES (?, ?, ?, ?)
    ''', (title, url, text, date))
    conn.commit()
    conn.close()

def get_all_users():

    with sqlite3.connect('bot_database.db') as conn:
        c = conn.cursor()
        c.execute('SELECT user_id FROM users')
        users = c.fetchone()  # Возвращает одну запись
        return users