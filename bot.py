from db import init_db, add_user, save_news_to_db, get_all_users
from parsing_vl import parser
from datetime import datetime, timedelta
import schedule
import threading
import telebot
import time

TOKEN = ''
bot = telebot.TeleBot(TOKEN)

init_db()

def run_bot():
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            print(f"Ошибка. Перезапуск через 5 секунд...")
            time.sleep(5)


@bot.message_handler(commands=['start'])
def start(message):
    user = message.from_user
    add_user(user.id, user.username, user.first_name, user.last_name)
    today_date = datetime.now().date()
    news = parser(today_date)
    if not news:
        bot.send_message(message.chat.id, 'Новостей за сегодня нет.')
    
    else: 
        bot.send_message(message.chat.id, 'Новости за сегодня:')
        for new in news:
            bot.send_message(message.chat.id, f'{new[0][0]}\n\n https://www.newsvl.ru{new[1][0]}')


def send_daily_news():
    date = (datetime.today() - timedelta(days=1)).date()
    news = parser(date)
    users = get_all_users()
    for user in users:
        bot.send_message(user, 'Новости за вчера:')
        for new in news:
            bot.send_message(user, f'{new[0][0]}\n\n https://www.newsvl.ru{new[1][0]}')
    
    print('Новости отправлены')





schedule.every().day.at("07:00").do(send_daily_news)

def run_scheduler():
    """
    Отдельный поток для работы планировщика.
    """
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    scheduler_thread = threading.Thread(target=run_scheduler, daemon=True)
    scheduler_thread.start()

    run_bot()