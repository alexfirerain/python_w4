import flask
from flask import jsonify, make_response, request

from . import db_session
from .news import News

blueprint = flask.Blueprint('news_api',
                            __name__,
                            template_folder='templates')


# @blueprint.errorhandler(400)
# def bad_request(_):
#     return make_response(jsonify({'error': 'Bad request'}), 400)
#
# @blueprint.errorhandler(404)
# def not_found(_):
#     return make_response(jsonify({'error': 'Not found'}), 404)

@blueprint.route('/api/news')
def get_news():
    db_sess = db_session.create_session()
    all_news = db_sess.query(News).all()

    return jsonify({
        'news': [item.to_dict(only=('title', 'content', 'user_id'))
                 for item in all_news]
    }
    )


# и передадим только нужные поля

@blueprint.route('/api/news/<int:news_id>', methods=['GET'])
def get_one_news(news_id):
    db_sess = db_session.create_session()
    news = db_sess.query(News).get(news_id)  # или через фильтр, или через .first()
    if not news:
        make_response(jsonify({'error': 'Never found'}), 404)
    return jsonify(
        {
            'news': news.to_dict(only=('title', 'content', 'user_id'))
        }
    )


# нужен ещё обработчик случая, если вместо id передали не число, а строку или т.д.
# напишем его здесь же (? а потом перенесли в main.py)

@blueprint.route('/api/news', methods=['POST'])
def create_news():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    if not all(key in request.json
                 for key in ['title', 'content', 'user_id', 'is_private']):  # т.е. проверка, что все необходимые поля
        return make_response(jsonify({'error': 'Not full request'}), 400)
    db_sess = db_session.create_session()
    news = News(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id'],
        is_private=request.json['is_private']
    )
    db_sess.add(news)
    db_sess.commit()
    return jsonify({'id': news.id})
# ну и там

@blueprint.route('/api/news/<int:news_id>', methods=['DELETE'])
def delete_news(news_id):
    db_sess = db_session.create_session()
    # news = db_sess.query(News).get(news_id)
    news = db_sess.get(News, news_id)
    if not news:
        return make_response(jsonify({'error': 'Never found'}), 404)
    db_sess.delete(news)
    db_sess.commit()
    return jsonify({'success': 'OK'})



"""
несклько вариков по АПИ

написали, оттестили.

SAS бесплатный остался только в VSCode,

НАДО научиться на лету наши объекты преобразовывать в JSON (словарь)
"""
