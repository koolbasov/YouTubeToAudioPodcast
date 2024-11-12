from bs4 import BeautifulSoup
import datetime
import os
from PIL import Image, ImageDraw, ImageFont
import requests
from sys import platform
import shutil
import textwrap
from yt_dlp.utils import DownloadError

from webapp import config
from webapp.db import db
from webapp.podcast.models import Feed, Podcast
from webapp.podcast.parser import converter_mp3


def create_cover(cover_text: str, playlist_id: str) -> str:
    img_template_path = os.path.join(config.basedir, "templates", config.COVER_TEMPLATE)
    img = Image.open(img_template_path)
    new_cover = ImageDraw.Draw(img)
    match platform:
        case "linux":
            FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        case "linux2":
            FONT = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
        case "darwin":
            FONT = "/Library/Fonts/Arial.ttf"
        case "win32":
            FONT = "arial.ttf"
    font = ImageFont.truetype(FONT, 250, encoding="UTF-8")
    lines = textwrap.wrap(cover_text, width=26)
    new_cover.multiline_text((100, 2400), "\n".join(lines), spacing=50, fill=(255, 255, 255), font=font)
    os.makedirs(config.feedimagedir, exist_ok=True)
    new_cover_name = playlist_id + ".jpg"
    new_cover_path = os.path.join(config.feedimagedir, new_cover_name)
    img.save(new_cover_path)
    return new_cover_name


def save_feed(
    user_id: int,
    feed_title: str,
    feed_link: str,
    lang_id: int,
    feed_description: str,
    feed_pubDate: datetime.datetime,
    lastBuildDate: datetime.datetime,
    feed_image: str,
) -> int:
    feed_exists = Feed.query.filter(Feed.feed_link == feed_link).count()
    if not feed_exists:
        new_feed = Feed(
            user_id=user_id,
            feed_title=feed_title,
            feed_link=feed_link,
            lang_id=lang_id,
            feed_description=feed_description,
            feed_pubDate=feed_pubDate,
            lastBuildDate=lastBuildDate,
            feed_image=feed_image,
        )
        db.session.add(new_feed)
        db.session.commit()
        return new_feed.id
    else:
        feed = Feed.query.filter(Feed.feed_link == feed_link).first()
        return feed.id


def image_download(image_url: str, image_prefix: str) -> str:
    os.makedirs(config.podcastimagedir, exist_ok=True)
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/126.0.0.0 Safari/537.36"
        )
    }
    image_content = requests.get(image_url, headers=headers, stream=True)
    image_name = image_prefix + ".jpg"
    image_path = os.path.join(config.podcastimagedir, image_name)
    with open(image_path, "wb") as image_file:
        shutil.copyfileobj(image_content.raw, image_file)
    return image_name


def save_podcasts(
    feed_id: int,
    podcast_title: str,
    ytb_link: str,
    ytb_description: str,
    enclosure: str | None,
    guid: str,
    pubDate: datetime.datetime,
    ytb_author: str,
    duration: int,
    ytb_image: str,
) -> None:
    podcast_exists = Podcast.query.filter(Podcast.ytb_link == ytb_link).count()
    if not podcast_exists:
        new_podcast = Podcast(
            feed_id=feed_id,
            podcast_title=podcast_title,
            ytb_link=ytb_link,
            ytb_description=ytb_description,
            enclosure=enclosure,
            guid=guid,
            pubDate=pubDate,
            ytb_author=ytb_author,
            duration=duration,
            ytb_image=ytb_image,
        )
        db.session.add(new_podcast)
        db.session.commit()


def download_and_save_all_feed_data(
    playlist_url: str,
    playlist_xml: str | None,
    playlist_html: str | None,
    playlist_id: str | None,
    language: int,
    user_id: int,
) -> None:
    if playlist_html and playlist_xml and playlist_id:
        soup_html = BeautifulSoup(playlist_html, "html.parser")
        soup_xml = BeautifulSoup(playlist_xml, "xml")
        all_items_xml = soup_xml.findAll("entry")

        # Fields for feed
        db_user_id = user_id
        feed_title = soup_html.find("meta", property="og:title")["content"]  # type: ignore
        feed_link = playlist_url
        db_language = language
        feed_description = soup_html.find("meta", property="og:description")["content"]  # type: ignore
        if not feed_description:
            feed_description = "No description"
        feed_pubDate = soup_xml.find("published").text  # type: ignore
        feed_pubDate = datetime.datetime.strptime(feed_pubDate, config.TIME_FORMAT_YOUTUBE)
        lastBuildDate = datetime.datetime.now(tz=datetime.timezone.utc)

        feed_image = create_cover(feed_title, playlist_id)  # type: ignore
        feed_id = save_feed(
            db_user_id, feed_title, feed_link, db_language, feed_description, feed_pubDate, lastBuildDate, feed_image  # type: ignore
        )

        # Fields for podcast
        for item in all_items_xml:
            ytb_podcast_id = item.find("yt:videoId").text
            podcast_title = item.find("title").text
            ytb_link = item.find("link")["href"]
            ytb_description = item.find("description").text
            guid = playlist_id + "::" + ytb_podcast_id
            pubDate = item.find("published").text
            pubDate = datetime.datetime.strptime(pubDate, config.TIME_FORMAT_YOUTUBE)
            ytb_author = item.find("author").text.strip()
            try:
                duration, enclosure = converter_mp3.download_and_convert_podcast(ytb_link, ytb_podcast_id, feed_title)  # type: ignore
            except DownloadError:
                duration = 0
                enclosure = None
            ytb_image = item.find("thumbnail")["url"]
            ytb_image = image_download(ytb_image, ytb_podcast_id)
            save_podcasts(
                feed_id,
                podcast_title,
                ytb_link,
                ytb_description,
                enclosure,
                guid,
                pubDate,
                ytb_author,
                duration,
                ytb_image,
            )
