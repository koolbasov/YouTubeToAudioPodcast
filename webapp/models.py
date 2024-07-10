from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()


class Feed(db.Model):
    __tablename__ = 'feed'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    feed_title = db.Column(db.String, nullable=False)
    feed_link = db.Column(db.String, unique=True, nullable=False)
    lang_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    feed_description = db.Column(db.String)
    feed_pubDate = db.Column(db.DateTime, nullable=False)
    lastBuildDate = db.Column(db.DateTime, nullable=False)
    feed_image = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Feed {}>'.format(self.feed_title, self.feed_link)


class Podcast(db.Model):
    __tablename__ = 'podcast'
    id = db.Column(db.Integer, primary_key=True)
    feed_id = db.Column(db.Integer, db.ForeignKey('feed.id'))
    podcast_title = db.Column(db.String, nullable=False)
    ytb_link = db.Column(db.String, unique=True, nullable=False)
    ytb_description = db.Column(db.String)
    enclosure = db.Column(db.String, nullable=False)
    guid = db.Column(db.String, nullable=False)
    pubDate = db.Column(db.DateTime, nullable=False)
    ytb_author = db.Column(db.String, nullable=False)
    duration = db.Column(db.Integer, nullable=False)
    ytb_image = db.Column(db.String, nullable=False)

    def __repr__(self):
        return '<Podcast {}>'.format(self.ytb_link, self.podcast_title)


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String(128))
    username = db.Column(db.String(64), index=True, nullable=False)
    role = db.Column(db.String(10), index=True)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.user_name)


class Language(db.Model):
    __tablename__ = 'languages'
    id = db.Column(db.Integer, primary_key=True)
    language = db.Column(db.String, nullable=False)
    identifier = db.Column(db.String, unique=True, nullable=False)

    def __repr__(self):
        return '<Language {}>'.format(self.language)
