from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo

class LoginForm(FlaskForm):
    username = StringField('Кличка', validators=[DataRequired("обязательное поле"), Length(min=4, max=20, message="от 4 до 20 символов")])
    password = PasswordField('Словечко', validators=[DataRequired("обязательное поле")])
    remember_me = BooleanField('Помнить меня')
    submit = SubmitField('Зайти')

#     для перевода ошибок на русский нужен некий транслятор, хотя можно тупо дать свои кастомные сообщения
# https://cont.ws/@Sage/503955/full
# https://www.geeksforgeeks.org/python/uploading-and-downloading-files-in-flask/?ysclid=md71k3iuq2445794126

