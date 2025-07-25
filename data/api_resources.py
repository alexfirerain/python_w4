# REST API по V2 уже с использованием flask-restful
# Работаем уже на уровне ресурсов, которые в нашем случае:
# Это - новости и пользователи
from flask import jsonify
from flask_restful import abort, Resource, reqparse
# аборт прерывает работу и возвращает ошибку (которая следом обрабатывается)


from data import db_session
from data.news import News


def abort_if_news_not_found(news_id):
    session = db_session.create_session()
    news = session.query(News).get(news_id)
    if not news:
        abort(404, error=f'Новость {news_id} не найдена')


# Этот ресурс читает или удаляет отдельную новость
class NewsResource(Resource):
    def get(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        return jsonify(
            {
                'news': news.to_dict(
                    only=('title', 'content', 'user_id', 'is_private'))
            }
        )

    def delete(self, news_id):
        abort_if_news_not_found(news_id)
        session = db_session.create_session()
        news = session.query(News).get(news_id)
        session.delete(news)
        session.commit()
        return jsonify({'success': f'Новость {news_id} удалена.'})


parser = reqparse.RequestParser()
parser.add_argument('title', required=True)
parser.add_argument('content', required=True)
parser.add_argument('is_private', required=True, type=bool)
parser.add_argument('user_id', required=True, type=int)

# получили все аргументы кортежем

class NewsResourceList(Resource):
    def get(self):
        session = db_session.create_session()
        news = session.query(News).all()
        return jsonify(
            {
                'news': [item.to_dict(
                    only=('title', 'content', 'user.name')) for item in news]
            }
        )

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        news = News(
            title=args['title'],
            content=args['title'],
            user_id=args['user_id'],
            is_private=args['is_private'],
        )
        session.add(news)
        session.commit()
        return jsonify({'id': news.id})