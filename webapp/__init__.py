import os.path

from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from webapp.models import db, User
from webapp.forms import LoginForm
from webapp.create_feed import feed_generator


def create_app():
    app = Flask(__name__, static_folder='rss')
    app.config.from_pyfile('config.py')
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route('/')
    def index():
        return "Youtube to RSS"

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        title = 'Вход'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(User.username == form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash('Вы успешно зашли на сайт')
                return redirect(url_for('index'))

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    @app.route('/admin')
    @login_required
    def admin_index():
        if current_user.is_admin:
            return 'admin'
        else:
            return 'У вас нет прав администратора'

    @app.route('/rss', methods=['GET', 'POST'])
    def rss_file():
        filename = feed_generator()
        filepath = f'/rss/{filename}'
        return render_template('rss.html', rss_file=filepath)

    return app
