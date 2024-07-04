import os
basedir = os.path.abspath(os.path.dirname(__file__))

RSS_TEMPLATE = "https://www.youtube.com/feeds/videos.xml?playlist_id="
TIME_FORMAT_DB = "%a, %d %b %Y %I:%M:%-S %z"
TIME_FORMAT_YOUTUBE = "%Y-%m-%dT%H:%M:%S%z"
ARTWORK_PATH = "youtubetopodcast-cover.jpg"
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, '..', 'webapp.db')
