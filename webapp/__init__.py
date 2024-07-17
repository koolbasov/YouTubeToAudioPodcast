from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from webapp.models import db, User
from webapp.forms import LoginForm, RegistrationForm
from webapp.create_feed import feed_generator
from webapp.decorators import admin_required


def create_app():
    app = Flask(__name__, static_folder='static')
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
        title = "YouTubeToAudioPodcast"
        return render_template('index.html', page_title=title)

    @app.route('/login')
    def login():
        if current_user.is_authenticated:
            return redirect(url_for('rss_file'))
        title = 'YouTubeToAudioPodcast | Вход'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash('Вы успешно вошли на сайт')
                return redirect(url_for('main'))

        flash('Неправильное имя пользователя или пароль')
        return redirect(url_for('login'))

    @app.route('/logout')
    def logout():
        logout_user()
        flash('Вы успешно разлогинились')
        return redirect(url_for('index'))

    @app.route('/admin_panel')
    @admin_required
    def admin_index():
        if current_user.is_admin:
            title = "YouTubeToAudioPodcast | Панель управления"
            return render_template('admin.html', page_title=title)
        else:
            return 'У вас нет прав администратора'

    @app.route('/rss')
    @login_required
    def rss_file():
        filename1 = feed_generator(1)
        filename2 = feed_generator(2)
        filepath1 = f'static/rss/{filename1}'
        filepath2 = f'static/rss/{filename2}'
        return render_template(
            'rss.html', rss_file1=filepath1,
            rss_file2=filepath2)

    @app.route('/register')
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('index'))
        form = RegistrationForm()
        title = "YouTubeToAudioPodcast | Регистрация"
        return render_template('registration.html', page_title=title, form=form)

    @app.route('/process-reg', methods=['POST'])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data, email=form.email.data, role='user')
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались')
            return redirect(url_for('login'))
        flash('Исправьте ошибки в форме')
        return redirect(url_for('register'))

    @app.route('/home')
    def main():
        title = "YouTubeToAudioPodcast | подкасты"
        return render_template('mainpage.html', page_title=title)

    return app
