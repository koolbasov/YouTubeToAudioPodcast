from flask import Flask, render_template
from flask_login import LoginManager

from webapp.db import db
from webapp.user.models import User
from webapp.admin.views import blueprint as admin_blueprint
from webapp.podcast.views import blueprint as podcast_blueprint
from webapp.user.views import blueprint as user_blueprint


def create_app():
    app = Flask(__name__, static_folder="static")
    app.config.from_pyfile("config.py")
    db.init_app(app)

    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = "user.login"
    app.register_blueprint(admin_blueprint)
    app.register_blueprint(podcast_blueprint)
    app.register_blueprint(user_blueprint)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(user_id)

    @app.route("/")
    def index():
        title = "YouTubeToAudioPodcast"
        return render_template("index.html", page_title=title)

    @app.errorhandler(404)
    def page_not_found(e):
        title = "YouTubeToAudioPodcast | 404 страница не найдена"
        return render_template("404.html", page_title=title), 404

    return app
