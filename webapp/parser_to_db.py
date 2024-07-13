from bs4 import BeautifulSoup
import datetime as dt
import os
import requests
import shutil
from yt_dlp.utils import DownloadError

import config
import converter_mp3
from models import db, Feed, Podcast


def image_download(image_url, image_prefix):
    image_folder = os.path.join("static", "img")
    os.makedirs(image_folder, exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                             "AppleWebKit/537.36 (KHTML, like Gecko) "
                             "Chrome/126.0.0.0 Safari/537.36"
               }
    image_content = requests.get(image_url, headers=headers, stream=True)
    image_name = image_prefix + ".jpg"
    image_path = os.path.join(image_folder, image_name + '.jpg')
    with open(image_path, 'wb') as image_file:
        shutil.copyfileobj(image_content.raw, image_file)
    return image_name


def parse_fields_for_data_base(
        playlist_url, playlist_xml, playlist_html,
        playlist_id, language=2, user_id=1):
    fields_for_db = []
    soup_html = BeautifulSoup(playlist_html, "html.parser")
    soup_xml = BeautifulSoup(playlist_xml, "xml")
    all_items_xml = soup_xml.findAll("entry")

    # Fields for feed
    db_user_id = user_id  # будет передан из базы данных при добавлении плейлиста
    feed_title = soup_html.find("meta", property="og:title")['content']
    feed_link = playlist_url
    db_language = language
    feed_description = soup_html.find("meta", property="og:description")['content']
    feed_pubDate = soup_xml.find("published").text
    feed_pubDate = dt.datetime.strptime(feed_pubDate, config.TIME_FORMAT_YOUTUBE)
    lastBuildDate = dt.datetime.now(tz=dt.timezone.utc)
    feed_image = config.ARTWORK_PATH
    feed_id = save_feed(
        db_user_id, feed_title, feed_link,
        db_language, feed_description,
        feed_pubDate, lastBuildDate, feed_image)

    # Fields for podcast
    for item in all_items_xml:
        ytb_podcast_id = item.find("yt:videoId").text
        podcast_title = item.find("title").text
        ytb_link = item.find("link")["href"]
        ytb_description = item.find("description").text
        guid = playlist_id + '::' + ytb_podcast_id
        pubDate = item.find("published").text
        pubDate = dt.datetime.strptime(pubDate, config.TIME_FORMAT_YOUTUBE)
        ytb_author = item.find("author").text.strip()
        try:
            duration, enclosure = converter_mp3.download_and_convert_podcast(
                ytb_link, ytb_podcast_id, feed_title)
        except DownloadError:
            duration = 0
            enclosure = None
        ytb_image = item.find("thumbnail")["url"]
        ytb_image = image_download(ytb_image, ytb_podcast_id)
        save_podcasts(
            feed_id, podcast_title, ytb_link, ytb_description, enclosure,
            guid, pubDate, ytb_author, duration, ytb_image)


def save_feed(
        user_id, feed_title, feed_link,
        lang_id, feed_description,
        feed_pubDate, lastBuildDate, feed_image):
    feed_exists = Feed.query.filter(Feed.feed_link == feed_link).count()
    if not feed_exists:
        new_feed = Feed(user_id=user_id, feed_title=feed_title,
                        feed_link=feed_link, lang_id=lang_id,
                        feed_description=feed_description,
                        feed_pubDate=feed_pubDate,
                        lastBuildDate=lastBuildDate,
                        feed_image=feed_image)
        db.session.add(new_feed)
        db.session.commit()
        return new_feed.id
    else:
        feed = Feed.query.filter(Feed.feed_link == feed_link).first()
        return feed.id


def save_podcasts(
        feed_id, podcast_title, ytb_link, ytb_description,
        enclosure, guid, pubDate, ytb_author, duration, ytb_image):
    podcast_exists = Podcast.query.filter(Podcast.ytb_link == ytb_link).count()
    if not podcast_exists:
        new_podcast = Podcast(
            feed_id=feed_id, podcast_title=podcast_title, ytb_link=ytb_link,
            ytb_description=ytb_description, enclosure=enclosure,
            guid=guid, pubDate=pubDate, ytb_author=ytb_author,
            duration=duration, ytb_image=ytb_image)
        db.session.add(new_podcast)
        db.session.commit()
