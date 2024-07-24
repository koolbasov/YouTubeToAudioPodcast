from flask_wtf import FlaskForm
from wtforms import (BooleanField, StringField, PasswordField,
                     SubmitField, SelectField)
from wtforms.validators import DataRequired, Email, EqualTo, ValidationError

from webapp.models import User
from webapp.get_xml_html import get_html_from_youtube


class LoginForm(FlaskForm):
    username = StringField('Логин', validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    password = PasswordField('Пароль', validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    remember_me = BooleanField('Запомнить меня', default=True,
                               render_kw={"class": "form-check-input"})
    submit = SubmitField('Войти',
                         render_kw={"class": "btn btn-warning"})


class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', validators=[DataRequired()],
                           render_kw={"class": "form-control"})
    email = StringField('Email', validators=[DataRequired(), Email()],
                        render_kw={"class": "form-control"})
    password = PasswordField("Пароль", validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(),
                                          EqualTo('password')],
                              render_kw={"class": "form-control"})
    submit = SubmitField("Зарегистрироваться",
                         render_kw={"class": "btn btn-warning"})

    def validate_username(self, username):
        users_count = User.query.filter_by(username=username.data).count()
        if users_count > 0:
            raise ValidationError(
                "Пользователь с таким именем уже зарегистрирован")

    def validate_email(self, email):
        users_count = User.query.filter_by(email=email.data).count()
        if users_count > 0:
            raise ValidationError(
                "Пользователь с такой электронной почтой уже зарегистрирован"
            )


class DownloadFeedForm(FlaskForm):
    feed_link = StringField('Вставьте ссылку для скачивания',
                            validators=[DataRequired()],
                            render_kw={"class": "form-control"})
    language = SelectField('Выберите язык', validate_choice=False,
                           render_kw={"class": "form-control"})
    submit = SubmitField('Загрузить плейлист',
                         render_kw={"class": "btn btn-warning"})

    def validate_feed_link(self, feed_link):
        is_youtube = "youtu.be" in feed_link.data or "youtube.com" in feed_link.data
        is_playlist = "playlist" in feed_link.data
        if not is_youtube:
            raise ValidationError(
                "Похоже это не ссылка на YouTube"
            )
        if not is_playlist:
            raise ValidationError(
                "Похоже это не плейлист"
            )
        if not get_html_from_youtube(feed_link.data):
            raise ValidationError(
                "Похоже вы пытаетесь загрузить private плейлист"
            )


class EditProfile(FlaskForm):
    password = PasswordField("Новый пароль", validators=[DataRequired()],
                             render_kw={"class": "form-control"})
    password2 = PasswordField('Повторите пароль',
                              validators=[DataRequired(),
                                          EqualTo('password')],
                              render_kw={"class": "form-control"})
    submit = SubmitField("Сохранить",
                         render_kw={"class": "btn btn-warning"})
