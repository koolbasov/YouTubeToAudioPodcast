from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user


from webapp.models import db, User, Feed
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
            return redirect(url_for('main'))
        title = 'YouTubeToAudioPodcast | Вход'
        login_form = LoginForm()
        return render_template('login.html', page_title=title, form=login_form)

    @app.route('/process-login', methods=['GET', 'POST'])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash('Вы успешно вошли на сайт')
                return redirect(url_for('login'))
        elif current_user.is_authenticated:
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

    @app.route('/register')
    def register():
        if current_user.is_authenticated:
            return redirect(url_for('main'))
        title = "YouTubeToAudioPodcast | Регистрация"
        form = RegistrationForm()
        return render_template('registration.html',
                               page_title=title, form=form)

    @app.route('/process-reg', methods=['GET', 'POST'])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data,
                            email=form.email.data, role='user')
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash('Вы успешно зарегистрировались')
            return redirect(url_for('login'))
        elif current_user.is_authenticated:
            return redirect(url_for('main'))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": - {}'.format(
                        getattr(form, field).label.text, error
                    ))
            return redirect(url_for('register'))

    @app.route('/home')
    @login_required
    def main():
        title = "YouTubeToAudioPodcast | подкасты"
        playlists = Feed.query.filter_by(user_id=current_user.id).all()
        rss_links = []
        for playlist in playlists:
            link = feed_generator(playlist.id)
            rss_links.append(link)
        return render_template('mainpage.html',
                               page_title=title, playlists=playlists,
                               rss_links=rss_links)

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    return app
