import csv

with open('people.csv', 'r', encoding='utf-8') as f:
    # кодировка здесь вот прям надо
    reader = csv.reader(f, delimiter=',', quotechar='"')
    # разделитель тоже может быть особым (по умолчанию запятая)
    # и расковычивания тоже
    for row in reader:
        print(row)

data = [
    ['Борис', '18', 'Бактрия'],
    ['Дзёмон', '27', 'Айну'],
    ['Бхасма', '34', 'Капсия'],
]

with open('dudes.csv', 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerows(data)
