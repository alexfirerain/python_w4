from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.fields.simple import EmailField, TextAreaField
from wtforms.validators import DataRequired


class Register(FlaskForm):
    email = EmailField('Эл-мыло', validators=[DataRequired("требуется корректное эл-мыло")])
    password = PasswordField('Пароль', validators=[DataRequired("требуется задать пароль")])
    password_repeat = PasswordField('Повторите пароль', validators=[DataRequired("ещё раз пароль")])
    name = StringField('Имя', validators=[DataRequired("требуется задать имя")])
    about = TextAreaField('Немног о себе')
    submit = SubmitField('Зарегистрироваться')
