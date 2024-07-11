import os
from feedgen.feed import FeedGenerator
import pytz

from webapp.models import Feed, Podcast, Language
from webapp import config


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
    filepath = os.path.join(config.basedir, f"rss/{filename}")
    fg.rss_file(filepath)
    return filename
