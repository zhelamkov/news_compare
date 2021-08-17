import requests
from bs4 import BeautifulSoup
import lxml
from time import sleep
import random
import json
import re
from bs4 import UnicodeDammit


response = requests.get('https://meduza.io/')
sleep(random.randint(0, 1))
dict_meduza = []

if response:
    print('start')
    soup = BeautifulSoup(response.content, 'lxml')
    news = soup.find_all('a', class_="Link-root Link-isInBlockTitle")
    counter = 0
    print(soup.original_encoding)
    for new in news:
        try:

            print(counter)
            counter += 1
            sleep(random.random())
            response_new = requests.get('https://meduza.io/' + new.get('href'))
            soup_page = BeautifulSoup(response_new.content, 'lxml')
            sleep(random.random())
            soup.original_encoding
            new_title_s = soup_page.find_all('p', class_='SimpleBlock-module_p__Q3azD')

            try:
                keyw = soup_page.find('head').find('meta', {'name': "keywords"}).get('content').split(', ')
            except:
                pass
            try:
                descr = soup_page.find('head').find('meta', {'name': "description"}).get('content').split()
            except Exceptions as e:
                print('Error descr:', e)
                pass

            title_text = ''
            for i in new_title_s:
                title_text += i.text.strip()

            print(new.get_text(strip=True))

            if title_text != '':
                dict_meduza.append({'Название статьи': new.get_text(strip=True),
                                    'Текст Статьи': title_text,
                                    'Ключевые слова': keyw,
                                    'Описание': descr
                                    })
        except:
            pass
with open('meduza_all.json', 'w', encoding="utf-8-sig") as file:
    json.dump(dict_meduza, file, indent=4, ensure_ascii=False)

print('finish')
