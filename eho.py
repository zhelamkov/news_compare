import requests
from bs4 import BeautifulSoup
import lxml
from time import sleep
import random
import json
import re
import datetime
from proxy_echo import proxies


days_new = 3
base = datetime.datetime.today()
date_list = [base - datetime.timedelta(days=x) for x in range(days_new)]
dates = []
for i in date_list:
    dates.append((i.strftime('%m %d')).split())
print(dates)

print('start')

news_links = []
for date in dates:
    sleep(random.randint(0, 10))
    headers = {'Accept': '*/*', 'user-agent': 'Chrome/91.0.4472.124'}

    response = requests.get(f'https://echo.msk.ru/news/2021/{date[0]}/{date[1]}/', proxies=proxies, headers=headers)
    sleep(random.randint(0, 1))
    if response:
        soup = BeautifulSoup(response.content, 'lxml')
        news_links.extend(soup.find_all('h3'))
counter = 0
dict_echo = []

for i in news_links[1:2]:
    sleep(random.randint(0, 2))
    page_title = i.find('a').text
    link = 'https://echo.msk.ru' + (i.find('a').get('href'))
    try:
        print(counter)
        counter += 1
        sleep(random.random())
        response_new = requests.get(link, proxies=proxies, headers=headers)
        soup_page = BeautifulSoup(response_new.content, 'lxml')
        text_page = soup_page.find('span', class_="_ga1_on_ include-relap-widget contextualizable").get_text(strip=True)

        try:
            title = soup_page.find('title').text
        except:
            pass
        try:
            descr = soup_page.find('head').find('meta', {'name': "description"}).get('content').strip()
            while descr[-1] == '…':
                descr = descr[:-1]
            descr = [i.lower() for i in descr.split()]
        except:
            print('Error descr')
            pass
        try:
            keyw = descr + title.split()
            keyw = [i.lower() for i in keyw if len(i) >= 2]
        except:
            pass

        if title != '':
            dict_echo.append({'Название статьи': title,
                              'Текст Статьи': text_page,
                              'Ключевые слова': keyw,
                              'Описание': descr
                              })
    except:
        pass

with open('echo_all.json', 'w', encoding="utf-8-sig") as file:
    json.dump(dict_echo, file, indent=4, ensure_ascii=False)

print('finish')
