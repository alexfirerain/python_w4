from flask_wtf import FlaskForm
from wtforms.fields.simple import StringField, TextAreaField, BooleanField
from wtforms.validators import DataRequired


class NewsForm(FlaskForm):
    title = StringField('Заголовок', validators=[DataRequired("Надо чтоб был заголовок")])
    content = TextAreaField('Содержание')
    is_private = BooleanField('Частная')
    submit = StringField('Применить')



