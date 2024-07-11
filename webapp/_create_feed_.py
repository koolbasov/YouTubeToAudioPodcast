from flask import Flask
from feedgen.feed import FeedGenerator
import pytz

from models import db, Feed, Podcast, Language
import config

app = Flask(__name__)
app.config.from_pyfile('config.py')
db.init_app(app)


def feed_generator(id=1):
    fg = FeedGenerator()
    fg.load_extension('podcast')

    my_feed = Feed.query.filter(Feed.id == id).first()
    fg.title(my_feed.feed_title)
    lang = Language.query.filter(Language.id == my_feed.lang_id).first()
    fg.language(lang.identifier)
    fg.link(href=f'{config.LOCAL_SITE_URL}/rss/{my_feed.feed_title}_{my_feed.id}.xml')
    fg.description(my_feed.feed_description)
    fg.pubDate(my_feed.feed_pubDate.replace(tzinfo=pytz.UTC))
    fg.lastBuildDate(my_feed.lastBuildDate.replace(tzinfo=pytz.UTC))
    fg.podcast.itunes_image(f"{config.LOCAL_SITE_URL}{my_feed.feed_image}")
    fg.podcast.itunes_author('Made by YoutubeToAudioPodcast')
    fg.podcast.itunes_explicit('no')

    # fe.load_extension('podcast')
    my_feed_podcasts = Podcast.query.filter(Podcast.feed_id == my_feed.id).all()
    for podcast in my_feed_podcasts:
        fe = fg.add_entry()
        fe.title(podcast.podcast_title)
        fe.link(href=podcast.ytb_link)
        fe.description(podcast.ytb_description)
        fe.enclosure(url=f"{config.LOCAL_SITE_URL}/{podcast.enclosure}", length=podcast.duration, type="audio/mpeg")
        fe.guid(podcast.guid)
        fe.pubDate(podcast.pubDate.replace(tzinfo=pytz.UTC))
        email, author = podcast.ytb_author.split('\n')
        fe.author({'name': author, 'email': email})
        fe.podcast.itunes_duration(podcast.duration)

    fg.rss_str(pretty=False)
    filename = f"{my_feed.feed_title}_{my_feed.id}.xml"
    filepath = f"rss/{my_feed.feed_title}_{my_feed.id}.xml"
    fg.rss_file(filepath)
    return filename


if __name__ == "__main__":
    with app.app_context():
        feed_generator()
