import requests
from bs4 import BeautifulSoup
import lxml
from time import sleep
import random
import json
import re
from proxy_echo import proxies


headers = {'Accept': 'accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9', 'user-agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Mobile Safari/537.36'}
print('start')

response = requests.get("https://rg.ru/include/tmpl-b-news-inner/is-announce/num-300/index.json", proxies=proxies, headers=headers)

if response:
    dict_rg = []
    rg_main = json.loads(response.text)
    for i in rg_main:
        try:
            kwd = [z.lower().strip('.,\"\/') for z in i['first_paragraph'].strip().split()]
            opis = [z.lower().strip('.,\"\/') for z in i['uannounce'].strip().split()]
            dict_rg.append({'Название статьи': i['link_title'],
                            'Текст Статьи': BeautifulSoup(i['text'], 'lxml').text,
                            'Ключевые слова': kwd,
                            'Описание': opis,
                            })
        except Exception as e:
            print(e)

with open('rg_all.json', 'w', encoding="utf-8-sig") as file:
    json.dump(dict_rg, file, indent=4, ensure_ascii=False)


print('finish')
