from flask import Blueprint, render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug import Response

from webapp.db import db
from webapp.user.forms import RegistrationForm, EditProfile
from webapp.user.forms import LoginForm
from webapp.user.models import User

blueprint = Blueprint("user", __name__, url_prefix="/users")


@blueprint.route("/login")
def login() -> str | Response:
    if current_user.is_authenticated:
        return redirect(url_for("podcast.main"))
    title = "YouTubeToAudioPodcast | Вход"
    login_form = LoginForm()
    return render_template("user/login.html", page_title=title, form=login_form)


@blueprint.route("/process-login", methods=["POST"])
def process_login() -> Response:
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            flash("Вы успешно вошли на сайт")
            return redirect(url_for("user.login"))
    elif current_user.is_authenticated:
        return redirect(url_for("podcast.main"))

    flash("Неправильное имя пользователя или пароль")
    return redirect(url_for("user.login"))


@blueprint.route("/logout")
def logout() -> Response:
    logout_user()
    flash("Вы успешно разлогинились")
    return redirect(url_for("index"))


@blueprint.route("/register")
def register() -> str | Response:
    if current_user.is_authenticated:
        return redirect(url_for("podcast.main"))
    title = "YouTubeToAudioPodcast | Регистрация"
    form = RegistrationForm()
    return render_template("user/registration.html", page_title=title, form=form)


@blueprint.route("/process-reg", methods=["POST"])
def process_reg() -> Response:
    form = RegistrationForm()
    if form.validate_on_submit():
        new_user = User(username=form.username.data, email=form.email.data, role="user")
        new_user.set_password(form.password.data)
        db.session.add(new_user)
        db.session.commit()
        flash("Вы успешно зарегистрировались")
        return redirect(url_for("user.login"))
    elif current_user.is_authenticated:
        return redirect(url_for("podcast.main"))
    else:
        for field, errors in form.errors.items():
            for error in errors:
                flash(f'Ошибка в поле "{getattr(form, field).label.text}": {error}')
        return redirect(url_for("user.register"))


@blueprint.route("/account", methods=["GET", "POST"])
@login_required
def account() -> str | Response:
    title = "YouTubeToAudioPodcast | мои данные"
    form = EditProfile()
    username = current_user.username
    email = current_user.email
    if form.validate_on_submit():
        new_user_data = User.query.filter_by(username=username).first()
        new_user_data.set_password(form.password.data)
        db.session.add(new_user_data)
        db.session.commit()
        flash("Данные успешно сохранены")
        return redirect(url_for("user.account"))
    for field, errors in form.errors.items():
        for error in errors:
            flash(f'Ошибка в поле "{getattr(form, field).label.text}": {error}')
    return render_template("user/account.html", page_title=title, form=form, username=username, email=email)
