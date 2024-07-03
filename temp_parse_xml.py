from bs4 import BeautifulSoup
import datetime as dt
import os
import requests
import shutil

import settings
import converter_mp3


with open("PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f.xml", "r", encoding="utf-8") as f:
    playlist_xml = f.read()

with open("PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f.html", "r", encoding="utf-8") as f:
    playlist_html = f.read()

playlist_url = "https://www.youtube.com/playlist?list=PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f"
playlist_id = "PLvO-3MXl8QMi98tFRoR0sqdVqOdQYX-9f"
# будет передан из базы данных при добавлении плейлиста
language = 2
# 1 - ru-ru, 2 - en-us, 3 - es ...

user_id = 1  # будет передан из базы данных при добавлении плейлиста
feed_id = 1  # будет передан из базы данных при добавлении плейлиста


def image_download(image_url, image_name):
    os.makedirs("img", exist_ok=True)
    image_content = requests.get(image_url, stream=True)
    image_path = os.path.join('img', image_name + '.jpg')
    with open(image_path, 'wb') as image_file:
        shutil.copyfileobj(image_content.raw, image_file)
    return image_path


fields_for_db = []

soup_html = BeautifulSoup(playlist_html, "html.parser")
soup_xml = BeautifulSoup(playlist_xml, "xml")
all_items = soup_xml.findAll("entry")

# Fields for feed
db_feed_id = feed_id  # будет передан из базы данных при добавлении плейлиста
db_user_id = user_id  # будет передан из базы данных при добавлении плейлиста
feed_title = soup_html.find("meta", property="og:title")['content']
feed_link = playlist_url
db_language = language
feed_description = soup_html.find("meta", property="og:description")['content']
feed_pubDate = soup_xml.find("published").text
feed_pubDate = dt.datetime.strptime(feed_pubDate, settings.TIME_FORMAT_YOUTUBE)
lastBuildDate = dt.datetime.now(tz=dt.timezone.utc)
feed_image = settings.ARTWORK_PATH

feed_fields_for_db = dict(
    id=db_feed_id,
    user_id=db_user_id,
    feed_title=feed_title,
    feed_link=feed_link,
    language=db_language,
    feed_description=feed_description,
    feed_pubDate=feed_pubDate,
    lastBuildDate=lastBuildDate,
    feed_image=feed_image
)

fields_for_db.append(feed_fields_for_db)

# Fields for podcast
for item in all_items:
    feed_id = db_feed_id  # будет передан из базы данных при добавлении плейлиста
    ytb_podcast_id = item.find("yt:videoId").text
    podcast_title = item.find("title").text
    ytb_link = item.find("link")["href"]
    ytb_description = item.find("description").text
    guid = playlist_id + '::' + ytb_podcast_id
    pubDate = item.find("published").text
    pubDate = dt.datetime.strptime(pubDate, settings.TIME_FORMAT_YOUTUBE)
    ytb_author = item.find("author").text.strip()
    duration, enclosure = converter_mp3.download_and_convert_podcast(
        ytb_link, ytb_podcast_id, feed_title)
    ytb_image = item.find("thumbnail")["url"]
    ytb_image = image_download(ytb_image, ytb_podcast_id)
    podcast_fields_for_db = dict(
        feed_id=feed_id,
        ytb_podcast_id=ytb_podcast_id,
        podcast_title=podcast_title,
        ytb_link=ytb_link,
        ytb_description=ytb_description,
        enclosure=enclosure,
        guid=guid,
        pubDate=pubDate,
        ytb_author=ytb_author,
        duration=duration,
        ytb_image=ytb_image
    )
    fields_for_db.append(podcast_fields_for_db)

print(fields_for_db)
