import json

# with open('rbc_all.json', 'r', encoding='utf-8-sig') as fl:
#    rbc=json.load(fl)
#    for i in rbc:
#        print(i)

print('=========')
with open('meduza_all.json', 'r', encoding='utf-8-sig') as fl:
    meduza = json.load(fl)
    for i in meduza:
        for j in i:
            print('==========')
            print(j)
            print(i[j], end='')
            print()
#dict_keys(['Название статьи', 'Текст Статьи', 'Ключевые слова', 'Описание'])






