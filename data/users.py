import datetime
import sqlalchemy as sa
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

from .db_session import SqlAlchemyBase
from sqlalchemy import orm

class User(SqlAlchemyBase, UserMixin):
    # если не указать __tablename__, то название таблицы будет равно имени класса
    __tablename__ = 'users'
    # Юзер-миксин - это класс, который автоматически добавляет в сущность поля id, is_active, is_anonymous, is_authenticated


    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    about = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, index=True, nullable=True, unique=True)
    hashed_password = sa.Column(sa.String, nullable=True)
    creation_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
    news = orm.relationship("News", back_populates="user")

    def __repr__(self):
        return f'User {self.name}'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

#      можно ещё счётчик неуспешных попыток входа (из реквеста возьмём ip адрес)


