import csv

# with open('people.csv', 'r', encoding='utf-8') as f:
#     # кодировка здесь вот прям надо
#     reader = csv.reader(f, delimiter=',', quotechar='"')
#     # разделитель тоже может быть особым (по умолчанию запятая)
#     # и расковычивания тоже
#     for row in reader:
#         print(row)
#
# data = [
#     ['Борис', '18', 'Бактрия'],
#     ['Дзёмон', '27', 'Айну'],
#     ['Бхасма', '34', 'Капсия'],
# ]
#
# with open('dudes.csv', 'w', encoding='utf-8', newline='') as f:
#     writer = csv.writer(f)
#     writer.writerows(data)

"""
Словарное чтение
"""
with open('people.csv', 'r', encoding='utf-8') as f:
    dic_reader = csv.DictReader(f)
    for row in dic_reader:
        print(row['name'], "тусуется в", row['motherland'])

field_names = ['name', 'age', 'motherland']
data_dic = {
    'name': 'Борис',
    'age': 38,
    'motherland': 'Тартария'
}
with open('staff.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=field_names)
    writer.writerow(data_dic)

data_per = ['name', 25, 'town']
with open('sample.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_NONNUMERIC)    # всё кавычит кроме чисел
    writer.writerow(data_per)
# ДЗ strtime, strptime