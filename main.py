# Введение въ Flask
import os
from datetime import datetime

import requests
# MVC - Model View Controller - Модель Представление Контроллер
# Фласк и есть такой фреймворк, минимально реализующий MVC
# ещё Джанго, там много всего.
# модель это хранимые данные, представление это что отображаем,
# а контроллер это тот, кто принимает запросы и отвечает
#
# шаблонизатор JINJA
#
from flask import Flask, url_for, request, render_template, redirect, abort
from werkzeug.utils import secure_filename
import sqlite3
from forms.login_form import LoginForm
from forms.news import NewsForm
from forms.user import Register
from data import db_session, news_api
from data.users import User
from data.news import News
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, login_required

# внутри Фласка есть сервер, на локальном хосте он кудахчет
# до тех пор, пока не остановишь

app = Flask(__name__)
debug = False
app.config['UPLOAD_FOLDER'] = 'uploads/'
app.config['SECRET_KEY'] = ('В пуранической истории пахтанья Молочного океана, дэвы и асуры'
                            'вели народ в пуране, и в пуране вели народ в пуране...'
                            'использовали Мандару как мутовку, а зме́я Васуки — как верёвку.')
ALLOWED_EXTENSIONS = {'txt', 'csv', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'zip', 'rar', '7z'}

login_manager = LoginManager()
login_manager.init_app(app)


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
    # visitor = current_user.name if current_user.is_authenticated else 'Юзер'
    params = {'title': 'Приветствие',
              'user': current_user.name if current_user.is_authenticated else 'Юзер',
              'weather': 'погодка ништяк'}
    return render_template('index.html', **params)


# колбэк-функция, возвращает браузеру ответ
# имя функции уникально на странице (пространство имён, понимаешь ли

@app.route('/about')
def about():  # имена функций уникальны
    print('Вызвана страница о нас')
    # if current_user.is_authenticated and current_user.is_admin():

    return render_template('about.html', title='О нас', user='посетитель')


# хороший тон это на 404 коде возвращать человеческое извинение
# статический контент — его просто так не добавишь, полагается ложить в папку static


@app.errorhandler(401)
def unauthorized(error):
    return redirect("/login"), 401  # либо дать страницу с описанием ситуаци


# для изображений, скриптов, мультимедиа, шрифтов, CSS и прочего надо свою папку static
# ДЗ что такое резет или нормалайз ЦСС, сначала поэтому резет, потом свои.
# чтоб постоянно не менять пути, есть url_for


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
    if num is None:
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
        db_sess = db_session.create_session()
        user = (db_sess.query(User)
                .filter(User.email == l_form.email.data).first())  # если нет, возвращает None
        if user and user.check_password(l_form.password.data):
            login_user(user, remember=l_form.remember_me.data)
            return redirect('/')
        else:
            return render_template('login.html',
                                   title='Вход',
                                   message='Неправильный логин или пароль',
                                   form=l_form), '401 UNAUTHORIZED'
    else:
        return render_template('login.html', title='Вход', form=l_form), '200 OK'


@login_manager.user_loader
def load_user(user_id):
    db_sess = db_session.create_session()
    return db_sess.query(User).get(user_id)


@app.route('/logout')
@login_required  # значит лишь авторизованные пользователи могут попасть на эту страницу
# чтоб юзер не увидел ошибку, сразу делаем редирект безусловный
def logout():
    logout_user()
    return redirect('/')


@app.route("/404")
def not_found(e):
    return render_template('404.html', title="Страница не найдена"), '404 NOT FOUND'


@app.route("/news")
def news():
    db_sess = db_session.create_session()
    if current_user.is_authenticated:
        all_public_news = db_sess.query(News).filter(
            (News.user == current_user) | (News.is_private != True)).all()  # ?
    else:
        all_public_news = db_sess.query(News).filter(
            (News.is_private != True)).all()
    # all_public_news = db_sess.query(News).filter(News.is_private == False).all()
    return render_template('news.html', title='Новости', news=all_public_news), '200 OK'


@app.route("/register", methods=['GET', 'POST'])
def register():
    reg_form = Register()
    if reg_form.validate_on_submit():  # эквивалентно, что request.method == 'POST'
        #  если пароли не совпали
        if reg_form.password.data != reg_form.password_repeat.data:
            return render_template('register.html',
                                   title='Давайте нормально региться',
                                   message="пароли не совпадают",
                                   form=reg_form), '406 NOT ACCEPTABLE'
        db_sess = db_session.create_session()
        # Если юзер с таким email уже есть
        if db_sess.query(User).filter(User.email == reg_form.email.data).first():
            return render_template('register.html',
                                   title='Давайте нормально региться',
                                   message="такой пользователь уже зареген",
                                   form=reg_form), '406 NOT ACCEPTABLE'
        user = User(
            name=reg_form.name.data,
            email=reg_form.email.data,
            about=reg_form.about.data,
        )
        user.set_password(reg_form.password.data)
        db_sess.add(user)
        db_sess.commit()
        # теперь безусловный редирект
        return redirect('/login')
    return render_template('register.html', title='Регистрация', form=reg_form), '200 OK'


@app.route('/newsmaking', methods=['GET', 'POST'])
@login_required
def make_news():
    news_form = NewsForm()
    if news_form.validate_on_submit():
        db_sess = db_session.create_session()
        piece_of_news = News()
        piece_of_news.title = news_form.title.data
        piece_of_news.content = news_form.content.data
        piece_of_news.is_private = news_form.is_private.data
        current_user.news.append(piece_of_news)
        db_sess.merge(current_user)
        db_sess.commit()
        return redirect('/news')
    return render_template('newsmaking.html', 'Добавление новости', form=news_form), '200 OK'


@app.route('/news/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_news(id_num):
    ed_form = NewsForm()
    if request.method == 'GET':
        db_sess = db_session.create_session()
        piece_of_news = db_sess.query(News).filter(
            News.id == id_num, News.user == current_user).first()
        if piece_of_news:
            ed_form.title.data = piece_of_news.title
            ed_form.content.data = piece_of_news.content
            ed_form.is_private.data = piece_of_news.is_private
        else:
            abort(404)
    if ed_form.validate_on_submit():
        db_sess = db_session.create_session()
        piece_of_news = db_sess.query(News).filter(
            News.id == id_num, News.user == current_user).first()
        if piece_of_news:
            piece_of_news.title = ed_form.title.data
            piece_of_news.content = ed_form.content.data
            piece_of_news.is_private = ed_form.is_private.data
            db_sess.commit()
            return redirect('/news')
        else:
            abort(404)
    return render_template('newsmaking.html', title='Работаем с новостью', form=ed_form), '200 OK'


@app.route('/newsdel/<int:id>')  # можно и метод DELETE
@login_required
def delete_news(id_num):
    db_sess = db_session.create_session()
    news = db_sess.query(News).filter(News.id == id_num, News.user == current_user).first()
    if news:
        # здесь ещё можно спросить, уверен ли он
        db_sess.delete(news)
        db_sess.commit()
    else:
        abort(404)
    return redirect('/news')

@app.route('/admin_page')
@login_required
def admin_page():
    if current_user.is_authenticated and current_user.is_admin():
        db_sess = db_session.create_session()
        all_news = db_sess.query(News).all()
        return render_template('admin_page.html', title='Админка', news=all_news), '200 OK'
    else:
        abort(404)


@app.route('/test-api')
def test_api():
    # ДЗ - вернуть это ещё встроенным в шаблон
    return requests.get('http://localhost:5000/api/news').json(), '200 OK'


# result = request.form


#     "контекст запроса" так называется тело ответа
# ДЗ <input type="reset"> и сабмит, а ещё посмотреть, что пишет какой браузер на кнопке по умолчанию
# ДЗ как закинуть файл на сервер (через форму)


# для запуска сервера импортируем app, вызываем run,
# эта строка должна быть в конце!
if __name__ == '__main__':
    db_session.global_init('db/news.sqlite')  # это подключает ORM
    app.register_blueprint(news_api.blueprint)
    app.run(host='localhost', port=5000, debug=debug)  # условно принят (в Докере 3000, ещё 8000 иногда)
    # приказы идут сверху вниз, подписи идут снизу вверх

    # db_sess = db_session.create_session()
    # first = db_sess.query(User).first()
    # print(first)
    # print(db_sess.query(User).all())
    # print(db_sess.query(User).filter(User.id > 1).first())
    #
    # # любые условия-предикаты в фильтр, причём можно через запятую вместо AND
    # db_sess.query(User).filter((User.id == 1), User.email.not_like("%a%")).all()
    # db_sess.query(User).filter((User.id != 1) | (User.email.not_like("%a%"))).all()
    #
    # # db_sess.query(User).filter(User.id == 2).first().name = 'Хуюзырь Батькыч'
    # # db_sess.commit()    # и все изменения, навороченные нами, улетели в БД!!!
    #
    # # db_sess.query(User).filter(User.id == 2).first().delete()  # удаление по id
    # # db_sess.commit()
    #
    # # user = db_sess.query(User).filter(User.id == 2).first()
    # # db_sess.delete(user)
    # db_sess.commit()
    #
    # # а вместо OR тогда у нас `|`
    #
    # # user = User()  # вот и стал доступным этот класс, ща по-простеньки
    # # user.name = 'Хуюзырь'
    # # user.about = 'данные о Хуюзыре'
    # # user.email = 'whoyuzy@yandex.ru'
    # # db_sess = db_session.create_session()  # открываем сессию работать с БД
    # # db_sess.add(user)
    # # db_sess.commit()  # сохраняем изменения в БД
    #
    # news = News(title='Ещё одна новость', content = 'Макарон объелся хохлопиздама', is_private=False, user_id=1)
    # # db_sess.add(news)
    # # db_sess.commit()
    #
    # user = db_sess.query(User).filter(User.id == 1).first()
    # user.news.append(news)  # добавляем новость в список новостей юзера!!!
    # db_sess.commit()

#     говорят, если в Юзере сделать репр возвращающим номер, то можно будет передать uesr_id=user
#  чтобы удалить юзера, сначала надо удалить все его связанные новости


# print(db_sess.query(News).filter(News.id == 2).first().content)

# for news in user.news:
#     print(f'{news.title}: {news.content}')

"""
Наследование шаблонов.
Надо сделать базовый для начала.

"""

"""
Юзера надо порадовать, когда 404 у него.
У сайта должен быть значок-пиктограмма: `.png` на прозрачном фоне, квадратная, размеры кратны 16

Яндекс ещё предлагает сделать svg 128x128 в кабинете вэбмастера, типа он на все будет рендериться.

А ещё метод дескрипшын.

DBeaver мощнейший, оверкильный.
"""

"""
# Как теперь ловить, кто зареген, кто не зареген?
is_authenticated()
сделать, чтоб когда залогинен, то вместо кнопки вход, кнопка выход
"""

"""
"Вэб приложение на Фласк-Питон" — это наш ключ к описанию нашего диплома.
Ничего "особо хорошего" делать не надо, это сделаем потом.
Сейчас надо сделать простой сайтец с базой данных.
Транслировать можно через "тоннель" съ своего компа, можно выйти к доске, или с места, или вообще.
Скачать методички с диска можно до 27 июля, сегодня там полный комплект материалов. 
см. также https://github.com/ipapMaster/flaskLessons
можно залить на 15 минут: https://github.com/ipapMaster/renderTest
ещё на Пайтон-энивэа можно разместить.


Как добавить фрагмент карты.

Есть Service Oriented Architecture (SOA), есть Microservices Architecture (MSA) как его реализация.
Архитектура "рассовываем по микросервисам":
Representational State Transfer (REST)
"мы с белков не работаем", надо сначала отрэмить.
у нас красные, а у них "синька".

"""
