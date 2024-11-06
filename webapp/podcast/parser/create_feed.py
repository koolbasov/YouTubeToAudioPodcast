import os
from feedgen.feed import FeedGenerator
import pytz

from webapp.podcast.models import Feed, Podcast, Language
from webapp import config


def feed_generator(feed_id):
    fg = FeedGenerator()
    fg.load_extension("podcast")

    my_feed = Feed.query.filter(Feed.id == feed_id).first()
    fg.title(my_feed.feed_title)
    lang = Language.query.filter(Language.id == my_feed.lang_id).first()
    fg.language(lang.identifier)
    fg.link(href=f"{config.LOCAL_SITE_URL}")
    fg.description(my_feed.feed_description)
    fg.pubDate(my_feed.feed_pubDate.replace(tzinfo=pytz.UTC))
    fg.lastBuildDate(my_feed.lastBuildDate.replace(tzinfo=pytz.UTC))
    fg.podcast.itunes_image(f"{config.LOCAL_SITE_URL}/static/covers/{my_feed.feed_image}")
    fg.podcast.itunes_author("Made by YoutubeToAudioPodcast")
    fg.podcast.itunes_explicit("no")

    my_feed_podcasts = Podcast.query.filter(Podcast.feed_id == my_feed.id).all()
    for podcast in my_feed_podcasts:
        fe = fg.add_entry()
        fe.title(podcast.podcast_title)
        fe.link(href=podcast.ytb_link)
        fe.description(podcast.ytb_description)
        fe.enclosure(
            url=f"{config.LOCAL_SITE_URL}/static/podcasts/{podcast.enclosure}",
            length=podcast.duration,
            type="audio/mpeg",
        )
        fe.guid(podcast.guid)
        fe.pubDate(podcast.pubDate.replace(tzinfo=pytz.UTC))
        email, author = podcast.ytb_author.split("\n")
        fe.author({"name": author, "email": email})
        fe.podcast.itunes_duration(podcast.duration)

    fg.rss_str(pretty=True)
    youtube_link = my_feed.feed_link
    url_id = youtube_link.split("list=")[1]
    filename = f"{url_id}.xml"
    file_folder = os.path.join(config.basedir, "static", "rss")
    os.makedirs(file_folder, exist_ok=True)
    file_path = os.path.join(file_folder, filename)
    fg.rss_file(file_path)
    return filename
