import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta



def parser(date):
    # URL страницы, которую парсим
    url = "https://www.newsvl.ru/" # замени на реальный адрес

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()

    # Парсим HTML
    soup = BeautifulSoup(response.text, 'html.parser')

    # Находим все блоки story-list__item
    stories = soup.find_all('div', class_='story-list__item')

    news = []
    
    for story in stories:
        # Извлекаем дату
        date_span = story.find('span', class_='story-list__item-date')
        date_text = date_span.get_text(strip=True) if date_span else "Неизвестно"
        story_date = date_pars(date_text)
        if story_date == date:
            # Извлекаем заголовок
            title_h3 = story.find('h3', class_='story-list__item-title')
            title = title_h3.get_text(strip=True) if title_h3 else "Без заголовка"

            # Извлекаем ссылку (из <a> внутри .story-list__item-content)
            link_a = story.find('div', class_='story-list__item-content').find('a', href=True)
            link = link_a['href'] if link_a else "#"
        
            news.append([[title], [link]])

    seen = set()
    sort_news = []
    for item in news:
        key = (item[0][0], item[1][0])
        if key not in seen:
            seen.add(key)
            sort_news.append(item)


    return sort_news

def date_pars(date_text):
    date_part = date_text.split(", ", 1)[-1]
    date_text_eng = date_part.replace("января", "January").replace("февраля", "February").replace("марта", "March").replace("апреля", "April").replace("мая", "May").replace("июня", "June").replace("июля", "July").replace("августа", "August").replace("сентября", "September").replace("октября", "October").replace("ноября", "November").replace("декабря", "December")
    story_date = datetime.strptime(date_text_eng, "%d %B %Y").date()
    return story_date

""""
#date = (datetime.today() - timedelta(days=1)).date()
print('вчера')
news = parser((datetime.today() - timedelta(days=1)).date())
print(news)
print('сегодня')
news = parser(datetime.today().date())
print(news)
"""
    

