import json

#  два метода читать: из файла `.load()`
# читать из строки (налету преобразовать и отправить, или вывести) `.loads()`

with open('dogs.json', encoding='utf-8') as d:
    data = json.load(d)  # т.е. создаёт словарь
    for i in range(len(data)):
        print(f'питомец № {i + 1}')
        for k, v in data[i].items():
            print(f'\t{k}: {v if type(v) != list else ', '.join(v)}')

    # temp = d.read()     # прочли как строку, без трактовки как словарь
    # data_s = json.loads(temp)   # теперче парсим строку в типа словарь
    #

fruit = {
    "ананас": 300,
    "банан": 400,
    "арбуз": 500,
    "киви": 600,
}

with open('fruits.json', 'w', encoding='utf-8') as f:
    json.dump(fruit, f, indent=4)   # записывает прям в файл

data = json.dumps(fruit) # а это просто сваливает словарь в строку
print(data)