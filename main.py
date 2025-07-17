# Введение въ Flask
import os

# MVC - Model View Controller - Модель Представление Контроллер
# Фласк и есть такой фреймворк, минимально реализующий MVC
# ещё Джанго, там много всего.
# модель это хранимые данные, представление это что отображаем,
# а контроллер это тот, кто принимает запросы и отвечает
#
# шаблонизатор JINJA
#
from flask import Flask, url_for, request, render_template
from werkzeug.utils import secure_filename
import sqlite3
from forms.login_form import LoginForm
from data import db_session

# внутри Фласка есть сервер, на локальном хосте он кудахчет
# до тех пор, пока не остановишь

app = Flask(__name__)
debug = False
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SECRET_KEY'] = ('В пуранической истории пахтанья Молочного океана, дэвы и асуры'
                            'вели народ в пуране, и в пуране вели народ в пуране...'
                            'использовали Мандару как мутовку, а зме́я Васуки — как верёвку.')
ALLOWED_EXTENSIONS = {'txt', 'csv', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'rar', '7z'}


def allowed_file(filename: str) -> bool:
    return ('.' in filename
            and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS)
    # два способа переноса в Питоне: через '\' или всё выражение в скобках (с 3.9)


# def secure_filename(filename: str) -> str:
#     return filename
#     # сделать перевод в допустимые символы

# для коммуникации с браузером юзаем декоратор @app.route
@app.route('/')
@app.route('/index')
def index():
    params = {}
    params['title'] = 'Приветствие'
    params['user'] = 'Юзер'
    params['weather'] = 'погодка ништяк'
    return render_template('index.html', **params)


# колбэк-функция, возвращает браузеру ответ
# имя функции уникально на странице (пространство имён, понимаешь ли

@app.route('/about')
def about():  # имена функций уникальны
    print('Вызвана страница о нас')
    return render_template('about.html', title='О нас', user='посетитель')


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
def greeting(user, user_id):
    return f'Привет, {user} с токеном {user_id}!<br>'


def _get_person(trip_id):
    connection = sqlite3.connect('db/persons.sqlite')
    cursor = connection.cursor()
    res = cursor.execute(f'SELECT name FROM users WHERE trip_id = {trip_id}').fetchone()
    cursor.close()
    connection.close()
    return res


@app.route('/trip/')  # но так лучше например вывести все имена
@app.route('/trip/<int:trip_id>')
def return_person(trip_id=None):
    if trip_id is None:
        return 'Не указан идентификатор поездки', '404 NOT FOUND'
    else:
        print(trip_id)
    return _get_person(trip_id)[0], '200 OK'


"""
ДЗ возвращать список всех имён если не указан id
return <a href="localhost:5000/get-user/{id-name}">ФИО</a>
    "нет номера записи" и список всех путёвок 
"""


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


# GET запрашивает данные, не меняя состояние сервера (read)
# POST отправляет данные на сервер (submit)
# PUT обновляет, (заменяет всё принудительно), данные на сервере (update)
# DELETE удаляет данные с сервера (delete)
# PATCH частично обновляет данные на сервере (update)

@app.route('/form', methods=['GET', 'POST'])
def form_test():
    if request.method == 'GET':
        with open('templates/form.html', 'r', encoding='utf-8') as h:
            return h.read()
    elif request.method == 'POST':
        result = request.form
        print(result['gender'])
        print(result['email'])
        print(result['accept'])
        print(result)

        file = request.files['file']
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))

        return "Форма успешно отправлена!<br>", '200 OK'
    return 'Такая тема не воспринимается сервером', '405 METHOD NOT ALLOWED'


@app.route('/upload', methods=['GET', 'POST'])
def file_upload():
    if request.method == 'GET':
        with open('templates/uploading.html', 'r', encoding='utf-8') as h:
            return h.read()
    elif request.method == 'POST':
        if 'file' not in request.files:
            return 'Файл не выбран', '400 BAD REQUEST'

        filename = request.files['file'].filename
        file = request.files['file']

        if filename == '':
            return 'Файл без имени', '400 BAD REQUEST'
        if file and allowed_file(filename):
            proper_name = secure_filename(filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], proper_name))
            return f'Файл {filename} успешно загружен!<br>'
    return 'Ошибка загрузки', '400 BAD REQUEST'


@app.route('/numbers')
@app.route('/numbers/<int:num>')
def odd_even(num=None):  # лучше конечно пусть имя функции совпадает с оконечником
    if num == None:
        return render_template('numbers.html', title='Нет числа, укажите его через "/число"',
                               number=''), '204 NO CONTENT'
    return render_template('numbers.html', title='Чёт/нечёт', number=num)


@app.route('/todo')
def todo():
    deals = ['Передать показания счётчика', 'Выгулять слона', 'Сходить за раскладом']
    return render_template('todo.html', deals=deals)


@app.route('/queue')
def queue():
    return render_template('vars.html', title='Очередь')


@app.route('/login', methods=['GET', 'POST'])
def login():
    l_form = LoginForm()
    if l_form.validate_on_submit():
        # если валидация прошла, значит то метод POST
        return f'Форма залита', '200 OK'
    else:
        return render_template('login.html', title='Вход', form=l_form), '200 OK'


# result = request.form


#     "контекст запроса" так называется тело ответа
# ДЗ <input type="reset"> и сабмит, а ещё посмотреть, что пишет какой браузер на кнопке по умолчанию
# ДЗ как закинуть файл на сервер (через форму)


# для запуска сервера импортируем app, вызываем run,
# эта строка должна быть в конце!
if __name__ == '__main__':
    db_session.global_init('db/news.sqlite')
    app.run(host='localhost', port=5000, debug=debug)  # условно принят (в Докере 3000, ещё 8000 иногда)
# приказы идут сверху вниз, подписи идут снизу вверх

"""
Наследование шаблонов.
Надо сделать базовый для начала.

"""
