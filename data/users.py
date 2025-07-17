import datetime
import sqlalchemy as sa
from .db_session import SqlAlchemyBase

class User(SqlAlchemyBase):
    # если не указать __tablename__, то название таблицы будет равно имени класса
    __tablename__ = 'users'

    id = sa.Column(sa.Integer, primary_key=True, autoincrement=True)
    name = sa.Column(sa.String, nullable=True)
    about = sa.Column(sa.String, nullable=True)
    email = sa.Column(sa.String, index=True, nullable=True, unique=True)
    hashed_password = sa.Column(sa.String, nullable=True)
    creation_date = sa.Column(sa.DateTime, default=datetime.datetime.now)
