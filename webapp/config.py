from datetime import timedelta
import os
basedir = os.path.abspath(os.path.dirname(__file__))

RSS_TEMPLATE = "https://www.youtube.com/feeds/videos.xml?playlist_id="
TIME_FORMAT_DB = "%a, %d %b %Y %I:%M:%-S %z"
TIME_FORMAT_YOUTUBE = "%Y-%m-%dT%H:%M:%S%z"
ARTWORK_PATH = "/covers/youtubetopodcast-cover.jpg"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
LOCAL_SITE_URL = "http://127.0.0.1:5000"

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "dh73920du2u02hfksjnfjsfh!@"

REMEMBER_COOKIE_DURATION = timedelta(days=14)
