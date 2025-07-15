"""
○ импорт sqlite3
○ подключились к БД
○ назначить "курсор" (бегунок)
○ работа с БД:
    ☼ делаем запрос
    ☼ коммитим
○ отключаемся от
"""
import sqlite3, csv

connection = sqlite3.connect('../db/movies.sqlite')
cursor = connection.cursor()

# result = cursor.execute(
#     """
#     SELECT year, COUNT(*) AS Кол_во
#     FROM films
#     GROUP BY year HAVING Кол_во > 500
#     ORDER BY Кол_во DESC
#     """)
# print(result.fetchall())  # список картежей очевидно
#
# res = cursor.execute('SELECT title, year FROM films WHERE year = 2010')
# # print(res.fetchall())
#
# for title, year in res.fetchall():
#     print(title, year)
#
# res = cursor.execute('SELECT title, year FROM films WHERE year BETWEEN 2001 AND 2005 ORDER BY duration')
#
# for title, year in res.fetchall():
#     print(title, year)
#
# answer = res.fetchone()  # вытягивает один (проверяет, есть ли, или если уже известно, что один)
# advice = res.fetchmany(5)  # сколько первых
#
# print(cursor.execute('SELECT title, year FROM films WHERE year BETWEEN 2001 AND 2007 ORDER BY year DESC').fetchmany(99))

"""
СОЗДАНИЕ ТАБЛИЦЫ
DDL есть Data Definition Language

INSERT INTO users(name, age) VALUES
    ('Ватыч', 21),
    ('Михася', 20)
    
UPDATE users SET age = 25 WHERE id=2
    
UPDATE users SET age = 22 WHERE name='Ватыч' # хотя в данном разе неправильно, ибо неоднозначно    

если есть поля необязательные (нулабельные), можно их не ставить вообще
можно менять сразу несколько, не вопрос:
UPDATE users SET name = 'Билли', age = 23 WHERE name = 'Билл'
удаление очевидно
DELETE FROM users WHERE age > 23
"""
# result = cursor.execute('UPDATE users SET age = 25 WHERE id=2') # переменная здесь просто так, ненужная
# изменения сохраняются не через бегунок, а через соеднение

# connection.execute('INSERT INTO users(name, age) VALUES ("Садхарта", 43), ("Юдыштыра", 39)')

with open('../14_июля/people.csv', 'r', encoding='utf-8') as f:
    reader = csv.reader(f, delimiter=',')
    next(reader)    # изящно пропускаем первую строку с заголовками столбцов
    # for row in range(1, len(reader)):
    #     cursor.execute(f'INSERT INTO users VALUES ({row[0]}, {row[1]})')
    # for name, age in reader:
    #     cursor.execute('INSERT INTO users(name, age) VALUES (?, ?)', (name, age))


# connection.commit()

"""
ALTER TABLE users ADD COLUMN city TEXT
DROP TABLE IF EXISTS users
CREATE TABLE IF NOT EXISTS users
ALTER TABLE users DROP COLUMN city
"""


connection.close()