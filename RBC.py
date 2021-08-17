import requests
from bs4 import BeautifulSoup
import lxml
from time import sleep
import random
import json
import re

headers = {'Accept': '*/*', 'user-agent': 'Chrome/91.0.4472.124'}
response = requests.get('https://meduza.io/', headers=headers)
my_id = BeautifulSoup(response.content, 'lxml')


companies = re.findall(r'\"datetime\":([\d]+)}', str(my_id.find('script')), flags=re.I)
page_id = (max([int(i) for i in companies]))

sleep(random.randint(0, 1))
response = requests.get(f'https://www.rbc.ru/v10/ajax/get-news-feed-short/project/rbcnews/lastDate/{page_id}/limit/99', headers=headers)

dict_rbc = []

if response:
    new = BeautifulSoup(response.content, 'lxml')
    news = (new.find_all('a', class_=r'\"item__link\"'))
    news = [(z.get('href')).replace('\\', '').replace('"', '') for z in news]

    spisok = ['www.rbc.ru', 'sportrbc.ru', 'quote.rbc.ru', 'realty.rbc.ru']

    news = [i for i in news if any([True if j in i else False for j in spisok])]
    counter = 0

    for new in news:

        print(counter)
        counter += 1
        try:
            response_new = requests.get(new)
            sleep(random.random())
            sleep(random.random())
            psoup_page = BeautifulSoup(response_new.content, 'lxml')
            new_title = psoup_page.find('h1', class_='article__header__title-in js-slide-title').text
            new_text = psoup_page.find('div', class_='article__text article__text_free')
            keyw = []
            try:
                keyw = psoup_page.find('head').find('meta', {'name': "keywords"}).get('content').split(', ')
            except:
                pass

            try:
                descr = psoup_page.find('head').find('meta', {'name': "description"}).get('content').split()
            except:
                print('Error descr')
                pass

            text_st = ''
            for i in new_text.find_all('p'):
                text_st += (i.text)
            print(new_title)
            if text_st != '':
                dict_rbc.append({'Название статьи': new_title,
                                 'Текст Статьи': text_st,
                                 'Ключевые слова': keyw,
                                 'Описание': descr,
                                 })

        except Exception as e:
            print('======================')
            print(e)
            print('======================')


# with open('news_meduza.txt', 'w', encoding="utf-8") as file:
#    for i in dict_meduza:
#        file.write(i.upper())  # .encode().decode('utf-8', 'ignore')
#        file.write(dict_meduza[i])

with open('rbc_all.json', 'w', encoding="utf-8-sig") as file:
    json.dump(dict_rbc, file, indent=4, ensure_ascii=False)


print('finish')
