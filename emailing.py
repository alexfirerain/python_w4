"""
чтоб отправить приложением мыло, нужен особый пароль
"я, мм, так сру" (яндекс-ру)

В Яндекс-кабинете взять пароль "для приложения" (будет показан единственный раз), ему дать название.
Погоду добавить умеем, ещё есть "поиск по карте"

ещё давайте пройдём управлением куками и сессиями ("хранилище" или "приложение")
печеньки у каждого есть, мы помним, где он сколько раз был, сталкерить юзера короче.

надо понимать, если, зачем мы это делаем
например чтобы заходить с того же места, где был, а не сначала
"""
import datetime

from flask import Flask, request, make_response, redirect, session

app = Flask(__name__)
app.config['SECRET_KEY'] = 'абракадабра'
# без этого сессия удаляется по закрытию браузера:
app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(hours=5)


@app.route('/')
def index():
    return redirect("/cookie_test")


@app.route('/cookie_test')
def cookie_test():
    visit_count = int(
        request.cookies.get('visit_count', 0))  # т.е. если этого ключа нет, то будет добавлен съ значением 0
    if visit_count:
        res = make_response(f'Вы здесь уже {visit_count} раз')
        res.set_cookie('visit_count', str(visit_count + 1),
                       max_age=60 * 60 * 24)  # заметим, что в печеньках только строки
    else:
        res = make_response('Вы здесь впервые')
        res.set_cookie('visit_count', '1', max_age=60 * 60 * 24)  # иначе пока открыт браузер (?)

    return res


# так же и с голосованием например
# минусы, что всё хранится открыто, можно быть удалено и т.д.
# корзину хранить там можно

"""
СЕССИИ
без секретного ключа не работает
"""
# вот здесь можно уже что-то секретное хранить


@app.route('/session_test')
def session_test():
    visit_count = session.get('visit_count', 0)
    session['visit_count'] = visit_count + 1
    # можно удалить сессию:
    # session.pop('visit_count', None)
    return f'Вы здесь уже {visit_count + 1} раз'



if __name__ == '__main__':
    app.run(host='localhost', port=8000)
