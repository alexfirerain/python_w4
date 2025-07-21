import flask
from flask import jsonify

from . import db_session
from .news import News

blueprint = flask.Blueprint('news_api',
                            __name__,
                            template_folder='templates')

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



"""
несклько вариков по АПИ

написали, оттестили.

SAS бесплатный остался только в VSCode,

НАДО научиться на лету наши объекты преобразовывать в JSON (словарь)
"""