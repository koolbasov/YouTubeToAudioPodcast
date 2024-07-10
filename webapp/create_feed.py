from flask import Flask
from feedgen.feed import FeedGenerator
import pytz

from models import db, Feed, Podcast, Language

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)

id = 1
with app.app_context():
    fg = FeedGenerator()
    fe = fg.add_entry()
    fe.load_extension('podcast')
    fg.load_extension('podcast')

    my_feed = Feed.query.filter(Feed.id == id).first()
    fg.title(my_feed.feed_title)
    lang = Language.query.filter(Language.id == my_feed.lang_id).first()
    fg.language(lang.identifier)
    fg.link(href=f'/webapp/{my_feed.feed_title}_{my_feed.id}.xml')
    fg.description(my_feed.feed_description)
    fg.pubDate(my_feed.feed_pubDate.replace(tzinfo=pytz.UTC))
    fg.lastBuildDate(my_feed.lastBuildDate.replace(tzinfo=pytz.UTC))
    fg.podcast.itunes_image(my_feed.feed_image)
    fg.podcast.itunes_author('Made by YoutubeToAudioPodcast')
    fg.podcast.itunes_explicit('no')


    my_feed_podcasts = Podcast.query.filter(Podcast.feed_id == my_feed.id).all()
    for podcast in my_feed_podcasts:
        fe.title(podcast.podcast_title)
        fe.link(href=podcast.ytb_link)
        fe.description(podcast.ytb_description)
        fe.enclosure(url=podcast.enclosure, length=podcast.duration, type="audio/mpeg")
        fe.guid(podcast.guid)
        fe.pubDate(podcast.pubDate.replace(tzinfo=pytz.UTC))
        email, author = podcast.ytb_author.split('\n')
        fe.author({'name': author, 'email': email})
        fe.podcast.itunes_duration(podcast.duration)

        fg.rss_file(f'{my_feed.feed_title}_{my_feed.id}.xml')

