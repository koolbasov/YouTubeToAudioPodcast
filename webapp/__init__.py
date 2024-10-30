from flask import Flask, render_template, flash, redirect, url_for
from flask_login import LoginManager, current_user, login_required, login_user, logout_user

from webapp.models import db, User, Feed, Language, Podcast
from webapp.forms import LoginForm, RegistrationForm, DownloadFeedForm, EditProfile
from webapp.create_feed import feed_generator
from webapp.decorators import admin_required
from webapp.get_xml_html import get_html_from_youtube
from webapp.parser_to_db import parse_fields_for_data_base
from webapp.languages_for_db import languages_for_form


def create_app():
    app = Flask(__name__, static_folder="static")
    app.config.from_pyfile("config.py")
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "login"

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        title = "YouTubeToAudioPodcast"
        return render_template("index.html", page_title=title)

    @app.route("/login")
    def login():
        if current_user.is_authenticated:
            return redirect(url_for("main"))
        title = "YouTubeToAudioPodcast | Вход"
        login_form = LoginForm()
        return render_template("login.html", page_title=title, form=login_form)

    @app.route("/process-login", methods=["GET", "POST"])
    def process_login():
        form = LoginForm()
        if form.validate_on_submit():
            user = User.query.filter_by(username=form.username.data).first()
            if user and user.check_password(form.password.data):
                login_user(user, remember=form.remember_me.data)
                flash("Вы успешно вошли на сайт")
                return redirect(url_for("login"))
        elif current_user.is_authenticated:
            return redirect(url_for("main"))

        flash("Неправильное имя пользователя или пароль")
        return redirect(url_for("login"))

    @app.route("/logout")
    def logout():
        logout_user()
        flash("Вы успешно разлогинились")
        return redirect(url_for("index"))

    @app.route("/admin_panel")
    @admin_required
    def admin_index():
        if current_user.is_admin:
            title = "YouTubeToAudioPodcast | Панель управления"
            return render_template("admin.html", page_title=title)
        else:
            return "У вас нет прав администратора"

    @app.route("/register")
    def register():
        if current_user.is_authenticated:
            return redirect(url_for("main"))
        title = "YouTubeToAudioPodcast | Регистрация"
        form = RegistrationForm()
        return render_template("registration.html", page_title=title, form=form)

    @app.route("/process-reg", methods=["GET", "POST"])
    def process_reg():
        form = RegistrationForm()
        if form.validate_on_submit():
            new_user = User(username=form.username.data, email=form.email.data, role="user")
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()
            flash("Вы успешно зарегистрировались")
            return redirect(url_for("login"))
        elif current_user.is_authenticated:
            return redirect(url_for("main"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
            return redirect(url_for("register"))

    @app.route("/home")
    @login_required
    def main():
        languages_set = languages_for_form()
        form = DownloadFeedForm()
        form.language.choices = languages_set
        title = "YouTubeToAudioPodcast | подкасты"
        playlists = Feed.query.filter_by(user_id=current_user.id).all()
        rss_links = []
        for playlist in playlists:
            link = feed_generator(playlist.id)
            rss_links.append(link)
        return render_template("mainpage.html", page_title=title, playlists=playlists, rss_links=rss_links, form=form)

    @app.route("/delete_playlist/<int:playlist_id>")
    @login_required
    def delete_playlist(playlist_id):
        playlist = Feed.query.filter_by(id=playlist_id).first()
        flash(f"Вы удалили плейлист  {playlist.feed_title}")
        db.session.delete(playlist)
        db.session.commit()
        return redirect(url_for("main"))

    @app.route("/download", methods=["GET", "POST"])
    @login_required
    def process_download():
        languages_set = languages_for_form()
        form = DownloadFeedForm()
        form.language.choices = languages_set
        if form.validate_on_submit():
            feed_link_data = form.feed_link.data
            language_data = form.language.data
            user_id_data = current_user.id
            playlist_xml, playlist_html, playlist_id = get_html_from_youtube(feed_link_data)
            flash("Ваш плейлист загружен")
            parse_fields_for_data_base(
                feed_link_data, playlist_xml, playlist_html, playlist_id, language_data, user_id_data
            )
            return redirect(url_for("main"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
            return redirect(url_for("main"))

    @app.route("/podcast/<int:podcast_id>")
    def podcast(podcast_id):
        title = "YouTubeToAudioPodcast | подкаст"
        try:
            my_podcasts = Podcast.query.filter(Podcast.feed_id == podcast_id).all()
            feed_title = Feed.query.filter(Feed.id == podcast_id).first().feed_title
            rss_link = feed_generator(podcast_id)
            return render_template(
                "podcast.html", page_title=title, feed_title=feed_title, podcasts=my_podcasts, rss_link=rss_link
            )
        except AttributeError:
            flash("Такого подкаста еще не загружено или он был удален")
            return redirect(url_for("main"))

    @app.route("/delete_podcast/<int:podcast_id>")
    @login_required
    def delete_podcast(podcast_id):
        podcast_to_delete = Podcast.query.filter_by(id=podcast_id).first()
        playlist_id = podcast_to_delete.feed_id
        flash(f"Вы удалили подкаст: {podcast_to_delete.podcast_title}")
        db.session.delete(podcast_to_delete)
        db.session.commit()
        return redirect(url_for("podcast", podcast_id=playlist_id))

    @app.route("/account", methods=["GET", "POST"])
    @login_required
    def account():
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
            return redirect(url_for("account"))
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    flash('Ошибка в поле "{}": - {}'.format(getattr(form, field).label.text, error))
        return render_template("account.html", page_title=title, form=form, username=username, email=email)

    @app.errorhandler(404)
    def page_not_found(e):
        title = "YouTubeToAudioPodcast | 404 страница не найдена"
        return render_template("404.html", page_title=title), 404

    return app


if __name__ == "__main__":
    app = create_app()
    app.run()
