from datetime import timedelta
import os

basedir = os.path.abspath(os.path.dirname(__file__))
podcastdir = os.path.join(basedir, "static", "podcasts")
podcastimagedir = os.path.join(basedir, "static", "img")
feedimagedir = os.path.join(basedir, "static", "covers")
rssfilesdir = os.path.join(basedir, "static", "rss")
headers = {
    "User-Agent": (
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/126.0.0.0 Safari/537.36"
    )
}

LANGUAGES = {
    "English": "en",
    "French": "fr",
    "German": "de",
    "Italian": "it",
    "Russian": "ru",
    "Spanish": "es",
}

RSS_TEMPLATE = "https://www.youtube.com/feeds/videos.xml?playlist_id="
TIME_FORMAT_DB = "%a, %d %b %Y %I:%M:%-S %z"
TIME_FORMAT_YOUTUBE = "%Y-%m-%dT%H:%M:%S%z"
COVER_TEMPLATE = "cover-template.jpg"
SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "..", "webapp.db")
LOCAL_SITE_URL = "http://127.0.0.1:5000"

SQLALCHEMY_TRACK_MODIFICATIONS = False

SECRET_KEY = "dh73lkjlkjlkjlkjkl**(*&(*72hfksjnfjsfh!@"

REMEMBER_COOKIE_DURATION = timedelta(days=7)
