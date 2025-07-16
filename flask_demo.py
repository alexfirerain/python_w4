# Введение въ Flask

# MVC - Model View Controller - Модель Представление Контроллер
# Фласк и есть такой фреймворк, минимально реализующий MVC
# ещё Джанго, там много всего.
# модель это хранимые данные, представление это что отображаем,
# а контроллер это тот, кто принимает запросы и отвечает
#
from flask import Flask, url_for, request
import sqlite3

# внутри Фласка есть сервер, на локальном хосте он кудахчет
# до тех пор, пока не остановишь

app = Flask(__name__)


# для коммуникации с браузером юзаем декоратор @app.route
@app.route('/')
@app.route('/index')
def index():
    return 'Привет, чуваки!'


# колбэк-функция, возвращает браузеру ответ
# имя функции уникально на странице (пространство имён, понимаешь ли

@app.route('/about')
def about():  # имена функций уникальны
    print('Вызвана страница о нас')
    return 'История о нас'


@app.route('/countdown')
def countdown():
    # в колбэке yield не работает
    lst = [str(x) for x in range(10, 0, -1)]
    lst.append('Поехали!')
    return '<br>'.join(lst)  # сервер (от колбэка) принимает только строку (не число)


# хороший тон это на 404 коде возвращать человеческое извинение
# статический контент — его просто так не добавишь, полагается ложить в папку static


@app.route('/image')
def show_image():
    # return f'<img src="static/img/map.jpg">'  # кросбраузерность и адаптивность это проблемы современной разработки (и поддержка старых браузеров)
    return f'<img src="{url_for('static', filename='img/map.jpg')}">'


# для изображений, скриптов, мультимедиа, шрифтов, CSS и прочего надо свою папку static
# ДЗ что такое резет или нормалайз ЦСС, сначала поэтому резет, потом свои.
# чтоб постоянно не менять пути, есть url_for

@app.route('/sample-page')
def sample_page():
    return f"""<!DOCTYPE html>
            <html lang="ru">
            <head>
                <meta charset="UTF-8">
                <title>Карта</title>
            </head>
            <body>
                <img src="{url_for('static', filename='img/map.jpg')}" alt="Python">
            </body>
            </html>
    """


@app.route('/sample-page2')
def sample_page2():
    with open('temp2.html', 'r', encoding='utf-8') as h:
        return h.read()

# @app.route('/form')
# def form():
#     with open('static/html/form.html', 'r', encoding='utf-8') as h:
#         return h.read()


# x = 5
# @app.route('/1')   # так не делаем конечно
# def show_num():
#     global x
#     x += 1
#     return str(x)

# <string> по умолчанию строка
# <int:number> - так передаём число
# <float:number> - так передаём вещественные числа
# <list> - так передаём список???
# <path:p> - может содержать слеши в пути!
# <uuid:id> - так передаём UUID, идентификатор 16 байт шестнадцатеричных, стандартный быстрый случайный
@app.route('/greeting/<user>/<int:id>')  # <user> - так правильно вносить все переменные
def greeting(user, id):
    return f'Привет, {user} с токеном {id}!<br>'




def get_person(trip_id):
    connection = sqlite3.connect('db/persons.sqlite')
    cursor = connection.cursor()
    res = cursor.execute(f'SELECT name FROM users WHERE trip_id = {trip_id}').fetchone()
    cursor.close()
    connection.close()
    return res

# name, city = result[0] - тка можно, распаковываем
# тогда return f"""<table>
#       <tr>
#           <td>ФИО</td>
#           <td>Город</td>
#       </tr>
#       <tr>
#           <td> {name}</td>
#           <td> {city}</td>
#       </tr>
#       </table>"""
# ДЗ проверю

@app.route('/trip/')    # но так лучше например вывести все имена
@app.route('/trip/<int:trip_id>')
def return_person(trip_id=None):
    if trip_id is None:
        return 'Не указан идентификатор поездки', '404 NOT FOUND'
    else:
        print(trip_id)
    return get_person(trip_id)[0], '200 OK'


# GET запрашивает данные, не меняя состояние сервера (read)
# POST отправляет данные на сервер (submit)
# PUT обновляет, (заменяет всё принудительно), данные на сервере (update)
# DELETE удаляет данные с сервера (delete)
# PATCH частично обновляет данные на сервере (update)

@app.route('/form', methods=['GET', 'POST'])
def form_test():
    if request.method == 'GET':
        with open('static/html/form.html', 'r', encoding='utf-8') as h:
            return h.read()
    elif request.method == 'POST':
        result = request.form
        print(result['gender'])
        print(result['email'])
        print(result['accept'])
        print(result)

        return "Форма успешно отправлена!<br>"

#     "контекст запроса" так называется тело ответа
# ДЗ <input type="reset"> и сабмит, а ещё посмотреть, что пишет какой браузер на кнопке по умолчанию
# ДЗ как закинуть файл на сервер (через форму)


# для запуска сервера импортируем app, вызываем run,
# эта строка должна быть в конце!
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=False)  # условно принят (в Докере 3000, ещё 8000 иногда)
# приказы идут сверху вниз, подписи идут снизу вверх
